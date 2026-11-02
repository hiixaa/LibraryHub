import pytest

from library import Library
from items import Book
from members import StudentMember
from errors import (
    DuplicateLoanError,
    LoanNotFoundError,
    UnpaidFinesError,
    RenewalNotAllowedError,
)


@pytest.fixture
def setup_library():
    library = Library()

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

    library.add_item(book)
    library.add_member(student)

    return library, book, student


def test_add_and_get_item(setup_library):
    library, book, student = setup_library

    assert library.get_item(book.isbn) == book


def test_add_and_get_member(setup_library):
    library, book, student = setup_library

    assert library.get_member("M001") == student


def test_borrow_book(setup_library):
    library, book, student = setup_library

    loan = library.borrow(book.isbn, student.member_id)

    assert loan in library.loans
    assert book.available_copies == 1


def test_duplicate_borrow(setup_library):
    library, book, student = setup_library

    library.borrow(book.isbn, student.member_id)

    with pytest.raises(DuplicateLoanError):
        library.borrow(book.isbn, student.member_id)


def test_return_book(setup_library):
    library, book, student = setup_library

    library.borrow(book.isbn, student.member_id)
    loan = library.return_item(book.isbn, student.member_id)

    assert loan.is_returned is True
    assert book.available_copies == 2


def test_return_without_active_loan(setup_library):
    library, book, student = setup_library

    with pytest.raises(LoanNotFoundError):
        library.return_item(book.isbn, student.member_id)


def test_renew_book(setup_library):
    library, book, student = setup_library

    loan = library.borrow(book.isbn, student.member_id)
    original_due_date = loan.due_date

    renewed_loan = library.renew(book.isbn, student.member_id)

    assert renewed_loan.due_date > original_due_date
    assert renewed_loan.renewal_count == 1


def test_borrow_with_unpaid_fines(setup_library):
    library, book, student = setup_library
    student.unpaid_fines = 101

    with pytest.raises(UnpaidFinesError):
        library.borrow(book.isbn, student.member_id)


def test_reserve_book(setup_library):
    library, book, student = setup_library

    book.available_copies = 0

    position = library.reserve(book.isbn, student.member_id)

    assert position == 1
    assert len(library.reservations) == 1


def test_member_loans(setup_library):
    library, book, student = setup_library

    loan = library.borrow(book.isbn, student.member_id)

    assert loan in library.member_loans(student.member_id)


def test_search_items(setup_library):
    library, book, student = setup_library

    results = library.search_items("wings")

    assert book in results


def test_list_items(setup_library):
    library, book, student = setup_library

    assert book in library.list_items()
    