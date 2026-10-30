from datetime import date, timedelta
from items import Book
from errors import RenewalNotAllowedError

class Loan:
    next_loan_number = 1

    def __init__(self, member, item, borrowed_date=None, loan_id=None):
        self.member = member
        self.item = item
        if loan_id is None:
            self.loan_id = f"L{Loan.next_loan_number:03d}"
            Loan.next_loan_number += 1
        else:
            self.loan_id = loan_id

        self.borrowed_date = borrowed_date or date.today()

        loan_days = item.loan_period(member)
        self.due_date = self.borrowed_date + timedelta(days=loan_days)

        self.returned_date = None
        self.renewal_count = 0


    @property
    def is_returned(self):
        return self.returned_date is not None

    def is_overdue(self, today):
        return today > self.due_date and not self.is_returned



    def renew(self):
        if self.is_returned:
            raise RenewalNotAllowedError(
                "Cannot renew a returned loan."
            )

        if not isinstance(self.item, Book):
            raise RenewalNotAllowedError(
                "This item cannot be renewed."
            )

        if self.renewal_count >= 2:
            raise RenewalNotAllowedError(
                "Maximum renewals reached."
            )

        self.due_date += timedelta(
            days=self.item.loan_period(self.member)
        )
        self.renewal_count += 1



    def return_item(self, returned_date=None):
        if self.is_returned:
            raise ValueError("Item has already been returned.")

        self.returned_date = returned_date or date.today()

    def __str__(self):
        return (
            f"Loan: {self.item.title} borrowed by "
            f"{self.member.name}, due on {self.due_date}"
        )

    
    def calculate_fine(self, returned_date):
        if returned_date <= self.due_date:
            return 0

        days_late = (returned_date - self.due_date).days
        fine = days_late * self.member.daily_fine_rate

        return min(fine, self.item.price)

    def __repr__(self):
        return (
            f"Loan(member={self.member!r}, "
            f"item={self.item!r}, "
            f"borrowed_date={self.borrowed_date!r}, "
            f"due_date={self.due_date!r})"
        )
