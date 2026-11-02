from datetime import date

from dsa.history import BorrowHistory
from items import Book
from members import StudentMember
from loans import Loan


def create_loan(number):
    member = StudentMember(
        f"M{number:03d}",
        f"Member {number}",
        f"member{number}@example.com",
    )

    item = Book(
        f"9780000000{number:03d}",
        f"Book {number}",
        ["Author"],
        "Fiction",
        200,
        300,
        1,
    )

    return Loan(member, item, date(2026, 10, 12))


def test_newest_loan_is_first():
    history = BorrowHistory()

    first = create_loan(1)
    second = create_loan(2)

    history.add(first)
    history.add(second)

    assert history.get_all() == [second, first]


def test_delete_existing_loan():
    history = BorrowHistory()

    first = create_loan(1)
    second = create_loan(2)

    history.add(first)
    history.add(second)

    assert history.delete(first.loan_id) is True
    assert history.get_all() == [second]


def test_delete_missing_loan():
    history = BorrowHistory()

    assert history.delete("L999") is False


def test_reverse_history():
    history = BorrowHistory()

    first = create_loan(1)
    second = create_loan(2)

    history.add(first)
    history.add(second)

    history.reverse()

    assert history.get_all() == [first, second]


def test_second_from_end():
    history = BorrowHistory()

    first = create_loan(1)
    second = create_loan(2)
    third = create_loan(3)

    history.add(first)
    history.add(second)
    history.add(third)

    assert history.second_from_end() == second


def test_second_from_end_with_one_loan():
    history = BorrowHistory()

    history.add(create_loan(1))

    assert history.second_from_end() is None


def test_empty_history():
    history = BorrowHistory()

    assert history.get_all() == []
    assert len(history) == 0
    assert history.second_from_end() is None