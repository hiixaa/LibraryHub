from datetime import date

from items import Book
from members import StudentMember
from library import Library


def setup_library():
    library = Library()

    book = Book(
        "9780000000011",
        "Wings of Fire",
        ["A. P. J. Abdul Kalam"],
        "Biography",
        200,
        350,
        1
    )

    member = StudentMember(
        "M001",
        "Asha Raman",
        "asha@example.com"
    )

    library.add_item(book)
    library.add_member(member)

    return library, book, member


def test_overdue_report():
    library, book, member = setup_library()

    loan = library.borrow(
        book.isbn,
        member.member_id,
        borrowed_date=date(2026, 9, 1)
    )

    overdue = library.overdue_report(date(2026, 10, 22))

    assert loan in overdue
    assert len(overdue) == 1


def test_due_date_is_not_overdue():
    library, book, member = setup_library()

    loan = library.borrow(
        book.isbn,
        member.member_id,
        borrowed_date=date(2026, 9, 1)
    )

    assert loan.is_overdue(loan.due_date) is False


def test_one_day_after_due_date_is_overdue():
    library, book, member = setup_library()

    loan = library.borrow(
        book.isbn,
        member.member_id,
        borrowed_date=date(2026, 9, 1)
    )

    day_after_due = date.fromordinal(
        loan.due_date.toordinal() + 1
    )

    assert loan.is_overdue(day_after_due) is True


def test_fine_on_due_date_is_zero():
    library, book, member = setup_library()

    loan = library.borrow(
        book.isbn,
        member.member_id,
        borrowed_date=date(2026, 9, 1)
    )

    assert loan.calculate_fine(loan.due_date) == 0


def test_fine_five_days_late():
    library, book, member = setup_library()

    loan = library.borrow(
        book.isbn,
        member.member_id,
        borrowed_date=date(2026, 9, 1)
    )

    late_date = date.fromordinal(
        loan.due_date.toordinal() + 5
    )

    assert loan.calculate_fine(late_date) == 10