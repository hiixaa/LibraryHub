import csv

from items import Book, ReferenceItem

from dsa.hashing import (
    import_books,
    group_by_author,
    most_borrowed,
    reading_challenge
)


def create_book(
    isbn,
    title,
    authors,
    pages,
    category="Programming"
):
    return Book(
        isbn,
        title,
        authors,
        category,
        pages,
        250.0,
        2,
        "Technology"
    )


def test_import_books_detects_duplicate(tmp_path, capsys):
    csv_path = tmp_path / "books.csv"

    rows = [
        [
            "9780000000011", "Wings of Fire",
            "A.P.J. Abdul Kalam;Arun Tiwari",
            "Biography", 180, 250, 2, "", "Book"
        ],
        [
            "9780000000011", "Duplicate Book",
            "Test Author", "Fiction", 200, 200, 2, "", "Book"
        ]
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "isbn", "title", "authors", "category",
            "pages", "price", "total_copies",
            "parent_category", "item_type"
        ])
        writer.writerows(rows)

    imported = import_books(csv_path)

    output = capsys.readouterr().out

    assert len(imported) == 1
    assert imported[0].title == "Wings of Fire"
    assert "Line 3: duplicate ISBN 9780000000011" in output
    assert "1 added, 1 duplicate skipped." in output


def test_import_books_supports_reference(tmp_path):
    csv_path = tmp_path / "books.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "isbn", "title", "authors", "category",
            "pages", "price", "total_copies",
            "parent_category", "item_type"
        ])

        writer.writerow([
            "9780000000066",
            "Encyclopaedia of Science",
            "Various",
            "Reference",
            1200,
            900,
            1,
            "",
            "Reference"
        ])

    imported = import_books(csv_path)

    assert len(imported) == 1
    assert imported[0].borrowable is False


def test_group_by_author():
    books = [
        create_book(
            "9780000000011",
            "Wings of Fire",
            ["A.P.J. Abdul Kalam", "Arun Tiwari"],
            180
        ),
        create_book(
            "9780000000042",
            "Python Crash Course",
            ["Eric Matthes"],
            544
        )
    ]

    result = group_by_author(books)

    assert result["A.P.J. Abdul Kalam"] == ["Wings of Fire"]
    assert result["Arun Tiwari"] == ["Wings of Fire"]
    assert result["Eric Matthes"] == ["Python Crash Course"]


def test_group_by_author_empty_list():
    assert group_by_author([]) == {}


def test_most_borrowed(tmp_path):
    books = [
        create_book("9780000000011", "Wings of Fire", ["Author"], 180),
        create_book("9780000000028", "The Alchemist", ["Author"], 208),
        create_book("9780000000035", "Clean Code", ["Author"], 464)
    ]

    loans_path = tmp_path / "loans.csv"

    with loans_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["loan_id", "member_id", "isbn"])

        writer.writerow(["L001", "M001", "9780000000011"])
        writer.writerow(["L002", "M002", "9780000000028"])
        writer.writerow(["L003", "M003", "9780000000011"])
        writer.writerow(["L004", "M004", "9780000000035"])
        writer.writerow(["L005", "M005", "9780000000028"])

    result = most_borrowed(loans_path, books, 3)

    assert result == [
        ("The Alchemist", 2),
        ("Wings of Fire", 2),
        ("Clean Code", 1)
    ]


def test_most_borrowed_empty_loans(tmp_path):
    books = [
        create_book("9780000000011", "Wings of Fire", ["Author"], 180)
    ]

    loans_path = tmp_path / "loans.csv"

    with loans_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["loan_id", "member_id", "isbn"])

    assert most_borrowed(loans_path, books) == []


def test_reading_challenge_724():
    books = [
        create_book("9780000000011", "Wings of Fire", ["Author"], 180),
        create_book("9780000000042", "Python Crash Course", ["Author"], 544)
    ]

    result = reading_challenge(books, 724)

    assert result is not None
    assert result[0].title == "Wings of Fire"
    assert result[1].title == "Python Crash Course"


def test_reading_challenge_720():
    books = [
        create_book("9780000000028", "The Alchemist", ["Author"], 208),
        create_book("9780000000059", "Sapiens", ["Author"], 512)
    ]

    result = reading_challenge(books, 720)

    assert result is not None
    assert result[0].title == "The Alchemist"
    assert result[1].title == "Sapiens"


def test_reading_challenge_no_pair():
    books = [
        create_book("9780000000011", "Wings of Fire", ["Author"], 180),
        create_book("9780000000028", "The Alchemist", ["Author"], 208)
    ]

    assert reading_challenge(books, 1000) is None


def test_reading_challenge_excludes_reference():
    reference = ReferenceItem(
        "9780000000066",
        "Encyclopaedia of Science",
        ["Various"],
        "Reference",
        1200,
        900.0,
        1
    )

    books = [
        reference,
        create_book("9780000000011", "Wings of Fire", ["Author"], 180)
    ]

    assert reading_challenge(books, 1380) is None