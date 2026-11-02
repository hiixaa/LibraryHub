import pytest
from items import Book, Magazine, ReferenceItem


def test_book_creation():
    book = Book(
        "9780000000011",
        "Wings of Fire",
        ["A.P.J. Abdul Kalam", "Arun Tiwari"],
        "Biography",
        180,
        250,
        2
    )

    assert book.title == "Wings of Fire"
    assert book.borrowable is True
    assert book.available_copies == 2


def test_magazine_creation():
    magazine = Magazine(
        "9780000000073",
        "India Today",
        ["Various"],
        "Magazines",
        90,
        80,
        3
    )

    assert magazine.title == "India Today"
    assert magazine.available_copies == 3


def test_reference_item_not_borrowable():
    reference = ReferenceItem(
        "9780000000066",
        "Encyclopaedia of Science",
        ["Various"],
        "Reference",
        1200,
        2500,
        1
    )

    assert reference.borrowable is False


def test_invalid_isbn():
    with pytest.raises(ValueError):
        Book(
            "123",
            "Invalid Book",
            ["Author"],
            "Fiction",
            100,
            200,
            1
        )

@pytest.mark.parametrize(
    "isbn",
    [
        "123",
        "123456789012",
        "abcdefghijklm",
        "978000000001"
    ]
)
def test_invalid_isbn_formats(isbn):
    with pytest.raises(ValueError):
        Book(
            isbn,
            "Test Book",
            ["Author"],
            "Fiction",
            100,
            200,
            1
        )

