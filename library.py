import csv
from datetime import date
from pathlib import Path
from items import LibraryItem
from members import StudentMember, RegularMember, PremiumMember
from loans import Loan
from datetime import date, timedelta
from items import Book, Magazine, ReferenceItem
from audit import audit
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
        # Instance attributes: each Library object has its own records.
        self.items = {}
        self.members = {}
        self.loans = []
        self.reservations = []
        self.last_notified_member = None
        self.audit_log = []

        # Set of ISBNs for quick membership checks.
        self.isbns = set()
        
    def load_data(self):
        data_folder = Path(__file__).parent

        # Load books
        with open(data_folder / "books.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                authors = row["authors"].split(";")

                item_type = row["item_type"]

                if item_type == "Book":
                    item = Book(
                        row["isbn"],
                        row["title"],
                        authors,
                        row["category"],
                        int(row["pages"]),
                        float(row["price"]),
                        int(row["total_copies"]),
                        row["parent_category"] or None
                    )
                elif item_type == "Magazine":
                    item = Magazine(
                        row["isbn"],
                        row["title"],
                        authors,
                        row["category"],
                        int(row["pages"]),
                        float(row["price"]),
                        int(row["total_copies"]),
                        row["parent_category"] or None
                    )
                elif item_type == "Reference":
                    item = ReferenceItem(
                        row["isbn"],
                        row["title"],
                        authors,
                        row["category"],
                        int(row["pages"]),
                        float(row["price"]),
                        int(row["total_copies"]),
                        row["parent_category"] or None
                    )
                else:
                    raise ValueError(f"Unknown item type: {item_type}")

                self.add_item(item)

        print(f"Loaded {len(self.items)} items.")

        
        # Load members
        with open(data_folder / "members.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                membership_type = row["membership_type"]

                if membership_type == "Student":
                    member = StudentMember(
                        row["member_id"], row["name"], row["email"]
                    )
                elif membership_type == "Regular":
                    member = RegularMember(
                        row["member_id"], row["name"], row["email"]
                    )
                elif membership_type == "Premium":
                    member = PremiumMember(
                        row["member_id"], row["name"], row["email"]
                    )
                else:
                    raise ValueError(
                        f"Unknown membership type: {membership_type}"
                    )

                self.add_member(member)

        print(f"Loaded {len(self.members)} members.")

        
        # Load loans
        with open(data_folder / "loans.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                member = self.get_member(row["member_id"])
                item = self.get_item(row["isbn"])

                issue_date = date.fromisoformat(row["issue_date"])
                due_date = date.fromisoformat(row["due_date"])
                return_date = (
                    date.fromisoformat(row["return_date"])
                    if row["return_date"]
                    else None
                )

                loan = Loan(member, item, issue_date, loan_id=row["loan_id"])
                loan.due_date = due_date
                loan.returned_date = return_date

                self.loans.append(loan)

            Loan.next_loan_number = max(
                int(loan.loan_id[1:])
                for loan in self.loans
                if loan.loan_id is not None
            ) + 1

            # Recalculate available copies based on active loans
            for item in self.items.values():
                active_loans = sum(
                    1
                    for loan in self.loans
                    if loan.item.isbn == item.isbn and not loan.is_returned
                )

                item.available_copies = item.total_copies - active_loans
            print(f"Loaded {len(self.loans)} loans.")
            
    # Load fines
        with open(data_folder / "fines.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                loan_id = row["loan_id"]
                amount = float(row["amount"])
                paid = row["paid"].strip().lower() == "yes"

                loan = next(
                    (loan for loan in self.loans if getattr(loan, "loan_id", None) == loan_id),
                    None
                )

                if loan is None:
                    print(f"Warning: Fine references unknown loan {loan_id}.")
                    continue

                if not paid:
                    loan.member.unpaid_fines += amount

        print(
            f"Loaded {len(self.items)} items, "
            f"{len(self.members)} members, "
            f"{len(self.loans)} loans, "
            f"{sum(1 for _ in open(data_folder / 'fines.csv', encoding='utf-8')) - 1} fines."
        )

    def add_item(self, item):
        if item.isbn in self.isbns:
            raise ValueError("An item with this ISBN already exists.")

        self.items[item.isbn] = item
        self.isbns.add(item.isbn)

    def add_member(self, member):
        if member.member_id in self.members:
            raise ValueError("A member with this ID already exists.")

        self.members[member.member_id] = member

    def get_item(self, isbn):
        if isbn not in self.items:
            raise ItemNotFoundError(f"Item {isbn} not found.")

        return self.items[isbn]

    def get_member(self, member_id):
        if member_id not in self.members:
            raise MemberNotFoundError(
                f"Member {member_id} not found."
            )

        return self.members[member_id]

    def list_items(self):
        return list(self.items.values())

    
    def search_items(self, search_term):
        search_term = search_term.strip().lower()

        return [
            item
            for item in self.items.values()
            if search_term in item.title.lower()
            or any(search_term in author.lower() for author in item.authors)
        ]


    def list_members(self):
        return list(self.members.values())

    @audit
    def borrow(self, isbn, member_id, borrowed_date=None):
        member = self.get_member(member_id)

        if not isinstance(isbn, str) or len(isbn) != 13 or not isbn.isdigit():
             raise InvalidISBNError("ISBN must be exactly 13 digits.")
        
        item = self.get_item(isbn)

        if not item.borrowable:
            raise ItemNotBorrowableError(
                "This item cannot be borrowed."
            )

        
        if member.unpaid_fines > 100:
            raise UnpaidFinesError(
                "Borrowing blocked: unpaid fines exceed ₹100."
            )


        if item.available_copies <= 0:
            raise ItemNotAvailableError(
                "No copies are available."
            )

        active_loans = [
            loan for loan in self.loans
            if loan.member.member_id == member_id
            and not loan.is_returned
        ]

        if len(active_loans) >= member.max_items:
            raise BorrowLimitExceededError(
                "Member has reached the borrowing limit."
            )

        
        for loan in active_loans:
            if loan.item.title.casefold()== item.title.casefold():
                raise DuplicateLoanError(
                    "Member already holds a copy of this title."
                )


        loan = Loan(member, item, borrowed_date)

        item.available_copies -= 1
        self.loans.append(loan)

        return loan

    @audit
    def return_item(self, isbn, member_id, returned_date=None):
        item = self.get_item(isbn)
        member = self.get_member(member_id)

        active_loan = None

        for loan in self.loans:
            if (
                loan.item.isbn == isbn
                and loan.member.member_id == member_id
                and not loan.is_returned
            ):
                active_loan = loan
                break

        if active_loan is None:
            raise LoanNotFoundError(
                "No active loan found for this member and item."
            )

        active_loan.return_item(returned_date)
        item.available_copies += 1

        self.last_notified_member = None

        for reservation in self.reservations:
            if reservation["isbn"] == isbn:
                self.last_notified_member = self.get_member(
                    reservation["member_id"]
                    )
                self.reservations.remove(reservation)
                break

        return active_loan

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
                waiting = any(
                    reservation["isbn"] == isbn
                    and reservation["member_id"] != member_id
                    for reservation in self.reservations
                )

                if waiting:
                    raise RenewalNotAllowedError(
                        f"{loan.item.title} cannot be renewed "
                        "because another member is waiting."
                    )
                for reservation in self.reservations:
                    if (
                        reservation["isbn"] == loan.item.isbn
                        and reservation["member_id"] != loan.member.member_id
                    ):
                        raise RenewalNotAllowedError(
                            f"'{loan.item.title}' cannot be renewed "
                            "because another member is waiting."
                        )


                loan.renew()
                return loan

        raise LoanNotFoundError(
            "No active loan found for this member and item."
        )

    
    def reserve(self, isbn, member_id):
        item = self.get_item(isbn)
        member = self.get_member(member_id)

        if item.available_copies > 0:
            raise ReservationError(
                "Reservation is only allowed when no copies are available."
            )

        for reservation in self.reservations:
            if (
                reservation["isbn"] == isbn
                and reservation["member_id"] == member_id
            ):
                raise ReservationError(
                    "Member has already reserved this item."
                )

        reservation = {
            "isbn": isbn,
            "member_id": member_id,
        }

        self.reservations.append(reservation)

        position = sum(
            1 for entry in self.reservations
            if entry["isbn"] == isbn
        )

        return position

    def get_waiting_list(self, isbn):
        self.get_item(isbn)

        return [
            self.get_member(reservation["member_id"])
            for reservation in self.reservations
            if reservation["isbn"] == isbn
        ]

    def member_loans(self, member_id):
        member = self.get_member(member_id)

        return [
            loan for loan in self.loans
            if loan.member.member_id == member.member_id
            and not loan.is_returned
        ]

    
    def iter_overdue(self, today):
        for loan in self.loans:
            if loan.is_overdue(today):
                yield loan

    
    def overdue_report(self, today):
        overdue_loans = list(self.iter_overdue(today))

        return sorted(
            overdue_loans,
            key=lambda loan: (today - loan.due_date).days,
            reverse=True
        )

    def items_by_category(self):
        categories = {
            item.category for item in self.items.values()
        }

        return {
            category: [
                item for item in self.items.values()
                if item.category == category
            ]
            for category in sorted(categories)
        }
    
    def members_with_fines(self):
        return [
            member for member in self.members.values()
            if member.unpaid_fines > 0
        ]







