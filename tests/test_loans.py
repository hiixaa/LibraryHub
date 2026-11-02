from datetime import date

import pytest

from items import Book
from members import StudentMember
from loans import Loan


@pytest.fixture
def loan():
    book = Book(
        "9780000000011",
        "Wings of Fire",
        ["A.P.J. Abdul Kalam"],
        "Biography",
        180,
        250,
        2
    )

    student = StudentMember(
        "M001",
        "Asha Raman",
        "asha@example.com"
    )

    return Loan(
        student,
        book,
        borrowed_date=date(2026, 10, 1)
    )


def test_loan_creation(loan):
    assert loan.borrowed_date == date(2026, 10, 1)
    assert loan.due_date == date(2026, 10, 15)
    assert loan.is_returned is False


def test_loan_renewal(loan):
    original_due_date = loan.due_date

    loan.renew()

    assert loan.renewal_count == 1
    assert loan.due_date > original_due_date


def test_loan_return(loan):
    loan.return_item(date(2026, 10, 20))

    assert loan.is_returned is True
    assert loan.returned_date == date(2026, 10, 20)


def test_returned_loan_cannot_be_renewed(loan):
    loan.return_item(date(2026, 10, 10))

    with pytest.raises(Exception):
        loan.renew()