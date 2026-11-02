
from collections import deque
from datetime import date, timedelta

from items import Book
from loans import Loan
from audit import audit
from dsa.history import BorrowHistory

from storage.object_mapper import ObjectMapper
from storage.loan_storage import LoanStorage

from errors import (
    InvalidISBNError,
    ItemNotFoundError,
    MemberNotFoundError,
    ItemNotBorrowableError,
    UnpaidFinesError,
    BorrowLimitExceededError,
    DuplicateLoanError,
    ItemNotAvailableError,
    LoanNotFoundError,
    ReservationError,
    RenewalNotAllowedError,
)


class Library:

    def __init__(self):
        self.items = {}
        self.members = {}
        self.loans = []

        self.reservations = []
        self.waiting_queues = {}

        self.last_notified_member = None
        self.audit_log = []
        self.isbns = set()

        self.undo_stack = []
        self.borrow_history = BorrowHistory()

        # Database integration
        self._persistent = False
        self._mapper = ObjectMapper()
        self._loan_storage = LoanStorage()

    # --------------------------------------------------
    # LOAD DATA FROM SQLITE
    # --------------------------------------------------

    def load_data(self):
        """Load all library data from the SQLite database."""

        self.items = self._mapper.load_items()
        self.members = self._mapper.load_members()

        self.loans = self._mapper.load_loans(
            self.members,
            self.items
        )

        self.isbns = set(self.items)

        self.reservations = []
        self.waiting_queues = {}

        self.undo_stack = []
        self.borrow_history = BorrowHistory()

        for loan in self.loans:
            self.borrow_history.add(loan)

        # Load fines.
        fine_count = 0

        for row in self._loan_storage.get_fines():

            fine_id, loan_id, amount, paid = row
            fine_count += 1

            if not paid:

                loan = next(
                    (
                        existing_loan
                        for existing_loan in self.loans
                        if existing_loan.loan_id == loan_id
                    ),
                    None
                )

                if loan:
                    loan.member.unpaid_fines += amount

        # Load waiting reservations.
        for row in self._loan_storage.get_reservations():

            (
                reservation_id,
                member_id,
                isbn,
                reservation_date,
                status
            ) = row

            self.reservations.append({
                "isbn": isbn,
                "member_id": member_id
            })

            self.waiting_queues.setdefault(
                isbn,
                deque()
            ).append(member_id)

        self._persistent = True

        print(f"Loaded {len(self.items)} items.")
        print(f"Loaded {len(self.members)} members.")
        print(f"Loaded {len(self.loans)} loans.")

        print(
            f"Loaded {len(self.items)} items, "
            f"{len(self.members)} members, "
            f"{len(self.loans)} loans, "
            f"{fine_count} fines."
        )

    # --------------------------------------------------
    # ADD ITEMS AND MEMBERS
    # --------------------------------------------------


    def add_item(self, item):

        if item.isbn in self.isbns:
            raise ValueError(
                "An item with this ISBN already exists."
            )

        # Save to database first.
        if self._persistent:
            self._mapper.add_item(item)

        # Update memory only after database success.
        self.items[item.isbn] = item
        self.isbns.add(item.isbn)


    def add_member(self, member):

        if member.member_id in self.members:
            raise ValueError(
                "A member with this ID already exists."
            )

        self.members[member.member_id] = member

    # --------------------------------------------------
    # GET ITEMS AND MEMBERS
    # --------------------------------------------------

    def get_item(self, isbn):

        if isbn not in self.items:
            raise ItemNotFoundError(
                f"Item {isbn} not found."
            )

        return self.items[isbn]

    def get_member(self, member_id):

        if member_id not in self.members:
            raise MemberNotFoundError(
                f"Member {member_id} not found."
            )

        return self.members[member_id]

    # --------------------------------------------------
    # LIST AND SEARCH
    # --------------------------------------------------

    def list_items(self):
        return list(self.items.values())

    def search_items(self, search_term):

        search_term = search_term.strip().lower()

        return [
            item
            for item in self.items.values()
            if (
                search_term in item.title.lower()
                or any(
                    search_term in author.lower()
                    for author in item.authors
                )
            )
        ]

    def list_members(self):
        return list(self.members.values())

    # --------------------------------------------------
    # BORROW
    # --------------------------------------------------

    @audit
    def borrow(self, isbn, member_id, borrowed_date=None):

        member = self.get_member(member_id)

        if (
            not isinstance(isbn, str)
            or len(isbn) != 13
            or not isbn.isdigit()
        ):
            raise InvalidISBNError(
                "ISBN must be exactly 13 digits."
            )

        item = self.get_item(isbn)

        if not item.borrowable:
            raise ItemNotBorrowableError(
                "This item cannot be borrowed."
            )

        if member.unpaid_fines > 100:
            raise UnpaidFinesError(
                "Borrowing blocked: unpaid fines exceed ₹100."
            )

        active_loans = [
            loan
            for loan in self.loans
            if (
                loan.member.member_id == member_id
                and not loan.is_returned
            )
        ]

        if len(active_loans) >= member.max_items:
            raise BorrowLimitExceededError(
                "Member has reached the borrowing limit."
            )

        for loan in active_loans:

            if loan.item.title.casefold() == item.title.casefold():
                raise DuplicateLoanError(
                    "Member already holds a copy of this title."
                )

        if item.available_copies <= 0:
            raise ItemNotAvailableError(
                "No copies are available."
            )

        loan = Loan(
            member,
            item,
            borrowed_date
        )

        # Save to database first.
        if self._persistent:

            try:
                self._loan_storage.borrow_transaction(loan)

            except Exception:
                Loan.next_loan_number -= 1
                raise

        # Update in-memory objects only after database success.
        item.available_copies -= 1

        self.loans.append(loan)
        self.borrow_history.add(loan)

        self.undo_stack.append({
            "action": "borrow",
            "loan": loan,
            "item": item
        })

        return loan

    # --------------------------------------------------
    # RETURN
    # --------------------------------------------------

    @audit
    def return_item(self, isbn, member_id, returned_date=None):

        item = self.get_item(isbn)
        member = self.get_member(member_id)

        active_loan = next(
            (
                loan
                for loan in self.loans
                if (
                    loan.item.isbn == isbn
                    and loan.member.member_id == member_id
                    and not loan.is_returned
                )
            ),
            None
        )

        if active_loan is None:
            raise LoanNotFoundError(
                "No active loan found for this member and item."
            )

        actual_return_date = returned_date or date.today()

        # Save previous state for undo.
        previous_queue = deque(
            self.waiting_queues.get(isbn, deque())
        )

        previous_reservations = [
            reservation.copy()
            for reservation in self.reservations
        ]

        previous_notification = self.last_notified_member
        previous_fines = member.unpaid_fines
        previous_return_date = active_loan.returned_date
        previous_available = item.available_copies

        fine_amount = active_loan.calculate_fine(
            actual_return_date
        )

        next_member_id = None

        # Perform database transaction first.
        if self._persistent:

            next_member_id = self._loan_storage.return_transaction(
                active_loan,
                actual_return_date,
                fine_amount
            )

            # Verify that both queues agree before changing memory.
            current_queue = self.waiting_queues.get(
                isbn,
                deque()
            )

            expected_member = (
                current_queue[0]
                if current_queue
                else None
            )

            if next_member_id != expected_member:
                raise RuntimeError(
                    "Database and in-memory reservation queues "
                    "are out of sync."
                )

        # Update the loan.
        active_loan.return_item(actual_return_date)

        if fine_amount > 0:
            member.unpaid_fines += fine_amount

        item.available_copies += 1

        # Notify the next member in the FIFO queue.
        self.last_notified_member = None

        queue = self.waiting_queues.setdefault(
            isbn,
            deque()
        )

        if queue:

            queued_member_id = queue.popleft()

            self.last_notified_member = self.get_member(
                queued_member_id
            )

            self.reservations = [
                reservation
                for reservation in self.reservations
                if not (
                    reservation["isbn"] == isbn
                    and reservation["member_id"] == queued_member_id
                )
            ]

        # Save undo information.
        self.undo_stack.append({
            "action": "return",
            "loan": active_loan,
            "item": item,
            "previous_return_date": previous_return_date,
            "previous_available": previous_available,
            "previous_queue": previous_queue,
            "previous_reservations": previous_reservations,
            "previous_notification": previous_notification,
            "previous_fines": previous_fines,
            "member": member
        })

        return active_loan

    # --------------------------------------------------
    # RENEW
    # --------------------------------------------------

    @audit
    def renew(self, isbn, member_id):

        self.get_item(isbn)
        self.get_member(member_id)

        for loan in self.loans:

            if (
                loan.item.isbn == isbn
                and loan.member.member_id == member_id
                and not loan.is_returned
            ):

                waiting = self.waiting_queues.get(
                    isbn,
                    deque()
                )

                if waiting:
                    raise RenewalNotAllowedError(
                        f"'{loan.item.title}' cannot be renewed "
                        "because another member is waiting."
                    )

                # Validate renewal before database update.
                if loan.renewal_count >= 2:
                    raise RenewalNotAllowedError(
                        "Maximum renewals reached."
                    )

                if not isinstance(loan.item, Book):
                    raise RenewalNotAllowedError(
                        "This item cannot be renewed."
                    )

                new_due_date = (
                    loan.due_date
                    + timedelta(days=loan.item.loan_period(loan.member))
                )

                new_count = loan.renewal_count + 1

                if self._persistent:
                    self._loan_storage.renew_transaction(
                        loan,
                        new_due_date,
                        new_count
                    )

                loan.renew()

                return loan

        raise LoanNotFoundError(
            "No active loan found for this member and item."
        )

    # --------------------------------------------------
    # RESERVATIONS
    # --------------------------------------------------

    def reserve(self, isbn, member_id):

        item = self.get_item(isbn)
        self.get_member(member_id)

        if item.available_copies > 0:
            raise ReservationError(
                "Reservation is only allowed when no copies are available."
            )

        queue = self.waiting_queues.setdefault(
            isbn,
            deque()
        )

        if member_id in queue:
            raise ReservationError(
                "Member has already reserved this item."
            )

        if self._persistent:
            self._loan_storage.reserve_transaction(
                isbn,
                member_id,
                date.today()
            )

        queue.append(member_id)

        self.reservations.append({
            "isbn": isbn,
            "member_id": member_id
        })

        return len(queue)

    def get_waiting_list(self, isbn):

        self.get_item(isbn)

        queue = self.waiting_queues.get(
            isbn,
            deque()
        )

        return [
            self.get_member(member_id)
            for member_id in queue
        ]

    # --------------------------------------------------
    # UNDO
    # --------------------------------------------------

    def undo(self):

        if not self.undo_stack:
            return None

        operation = self.undo_stack[-1]
        action = operation["action"]

        if action == "borrow":

            loan = operation["loan"]
            item = operation["item"]

            if self._persistent:
                self._loan_storage.undo_borrow_transaction(loan)

            self.undo_stack.pop()

            if loan in self.loans:
                self.loans.remove(loan)

            item.available_copies += 1

            self.borrow_history.delete(loan.loan_id)

            return {
                "action": "borrow",
                "loan": loan
            }

        if action == "return":

            loan = operation["loan"]
            item = operation["item"]
            member = operation["member"]

            if self._persistent:
                self._loan_storage.undo_return_transaction(
                    loan,
                    operation["previous_queue"]
                )

            self.undo_stack.pop()

            loan.returned_date = operation["previous_return_date"]

            item.available_copies = operation["previous_available"]

            self.waiting_queues[loan.item.isbn] = deque(
                operation["previous_queue"]
            )

            self.reservations = [
                reservation.copy()
                for reservation in operation["previous_reservations"]
            ]

            self.last_notified_member = operation["previous_notification"]

            member.unpaid_fines = operation["previous_fines"]

            return {
                "action": "return",
                "loan": loan
            }

        return None

    # --------------------------------------------------
    # BORROW HISTORY
    # --------------------------------------------------

    def get_borrow_history(self):
        return self.borrow_history.get_all()

    def delete_history(self, loan_id):
        return self.borrow_history.delete(loan_id)

    def reverse_history(self):
        self.borrow_history.reverse()

    def second_last_borrow(self):
        return self.borrow_history.second_from_end()

    # --------------------------------------------------
    # REPORTS
    # --------------------------------------------------

    def member_loans(self, member_id):

        member = self.get_member(member_id)

        return [
            loan
            for loan in self.loans
            if (
                loan.member.member_id == member.member_id
                and not loan.is_returned
            )
        ]

    def iter_overdue(self, today):

        for loan in self.loans:

            if loan.is_overdue(today):
                yield loan

    def overdue_report(self, today):

        return sorted(
            list(self.iter_overdue(today)),
            key=lambda loan: (today - loan.due_date).days,
            reverse=True
        )

    def items_by_category(self):

        categories = {
            item.category
            for item in self.items.values()
        }

        return {
            category: [
                item
                for item in self.items.values()
                if item.category == category
            ]
            for category in sorted(categories)
        }

    def members_with_fines(self):

        return [
            member
            for member in self.members.values()
            if member.unpaid_fines > 0
        ]
