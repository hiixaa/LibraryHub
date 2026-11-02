
from datetime import date
from collections import defaultdict, deque

from items import Book, Magazine, ReferenceItem
from members import StudentMember, RegularMember, PremiumMember
from loans import Loan

from storage.item_storage import ItemStorage
from storage.member_storage import MemberStorage
from storage.loan_storage import LoanStorage


class ObjectMapper:

    def __init__(self):
        self.item_storage = ItemStorage()
        self.member_storage = MemberStorage()
        self.loan_storage = LoanStorage()

    
    # --------------------------------------------------
    # SAVE NEW ITEM
    # --------------------------------------------------

    def add_item(self, item):
        """Save a library item to the database."""

        item_types = {
            Book: "Book",
            Magazine: "Magazine",
            ReferenceItem: "Reference"
        }

        item_type = item_types[type(item)]

        self.item_storage.add({
            "isbn": item.isbn,
            "title": item.title,
            "item_type": item_type,
            "category": item.category,
            "pages": item.pages,
            "price": item.price,
            "total_copies": item.total_copies,
            "authors": item.authors
        })


    # --------------------------------------------------
    # LOAD ITEMS
    # --------------------------------------------------

    def load_items(self):
        items = {}

        item_classes = {
            "Book": Book,
            "Magazine": Magazine,
            "Reference": ReferenceItem
        }

        for row in self.item_storage.get_all():

            (
                isbn,
                title,
                item_type,
                category,
                pages,
                price,
                total_copies,
                parent_category
            ) = row

            authors = self.item_storage.get_authors(isbn)

            item_class = item_classes[item_type]

            item = item_class(
                isbn,
                title,
                authors,
                category,
                pages,
                price,
                total_copies,
                parent_category
            )

            items[isbn] = item

        return items

    # --------------------------------------------------
    # LOAD MEMBERS
    # --------------------------------------------------

    def load_members(self):
        members = {}

        member_classes = {
            "Student": StudentMember,
            "Regular": RegularMember,
            "Premium": PremiumMember
        }

        for row in self.member_storage.get_all():

            (
                member_id,
                name,
                email,
                membership_type,
                loan_limit,
                loan_period,
                fine_per_day
            ) = row

            member_class = member_classes[membership_type]

            member = member_class(
                member_id,
                name,
                email
            )

            members[member_id] = member

        return members

    # --------------------------------------------------
    # LOAD LOANS
    # --------------------------------------------------

    def load_loans(self, members, items):
        loans = []

        for row in self.loan_storage.get_all():

            (
                loan_id,
                member_id,
                member_name,
                isbn,
                item_title,
                issue_date,
                due_date,
                return_date,
                renewal_count
            ) = row

            member = members[member_id]
            item = items[isbn]

            borrowed_date = date.fromisoformat(issue_date)

            loan = Loan(
                member,
                item,
                borrowed_date,
                loan_id=loan_id
            )

            loan.due_date = date.fromisoformat(due_date)

            loan.returned_date = (
                date.fromisoformat(return_date)
                if return_date
                else None
            )

            loan.renewal_count = renewal_count

            loans.append(loan)

        # Continue generating IDs after the largest existing ID.
        if loans:
            Loan.next_loan_number = max(
                int(loan.loan_id[1:])
                for loan in loans
            ) + 1
        else:
            Loan.next_loan_number = 1

        # Recalculate available copies using active loans.
        for item in items.values():

            active_count = sum(
                1
                for loan in loans
                if loan.item.isbn == item.isbn
                and not loan.is_returned
            )

            item.available_copies = (
                item.total_copies - active_count
            )

        return loans

    # --------------------------------------------------
    # LOAD FINES
    # --------------------------------------------------

    def load_fines(self, members):
        fine_count = 0

        for row in self.loan_storage.get_fines():

            fine_count += 1

            fine_id, loan_id, amount, paid = row

            if not paid:

                loan = self.loan_storage.get_by_id(loan_id)

                if loan:
                    member_id = loan[1]

                    if member_id in members:
                        members[member_id].unpaid_fines += amount

        return fine_count

    # --------------------------------------------------
    # LOAD RESERVATIONS
    # --------------------------------------------------

    def load_reservations(self):
        reservations = []
        waiting_queues = defaultdict(deque)

        for row in self.loan_storage.get_reservations():

            (
                reservation_id,
                member_id,
                isbn,
                reservation_date,
                status
            ) = row

            reservation = {
                "reservation_id": reservation_id,
                "member_id": member_id,
                "isbn": isbn,
                "reservation_date": reservation_date,
                "status": status
            }

            reservations.append(reservation)
            waiting_queues[isbn].append(member_id)

        return reservations, dict(waiting_queues)
