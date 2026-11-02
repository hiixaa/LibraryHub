from items import Book

from dsa.search import (
    linear_search_by_title,
    binary_search
)

from dsa.sorting import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    catalogue_sort,
    top_level_category
)


def sample_books():
    return [
        Book(
            "9780000000011",
            "Wings of Fire",
            ["A.P.J. Abdul Kalam"],
            "Biography",
            180,
            250.0,
            2
        ),
        Book(
            "9780000000028",
            "The Alchemist",
            ["Paulo Coelho"],
            "Fiction",
            208,
            250.0,
            2
        ),
        Book(
            "9780000000035",
            "Clean Code",
            ["Robert C. Martin"],
            "Software Engineering",
            464,
            500.0,
            2,
            "Technology"
        ),
        Book(
            "9780000000042",
            "Python Crash Course",
            ["Eric Matthes"],
            "Programming",
            544,
            450.0,
            2,
            "Technology"
        )
    ]


# Linear search tests

def test_linear_search_found():
    books = sample_books()

    assert linear_search_by_title(
        books,
        "Wings of Fire"
    ) == 0


def test_linear_search_case_insensitive():
    books = sample_books()

    assert linear_search_by_title(
        books,
        "clean code"
    ) == 2


def test_linear_search_not_found():
    books = sample_books()

    assert linear_search_by_title(
        books,
        "Cooking"
    ) == -1


def test_linear_search_empty_list():
    assert linear_search_by_title([], "Python") == -1


# Binary search tests

def test_binary_search_found():
    isbns = [
        "9780000000011",
        "9780000000028",
        "9780000000035",
        "9780000000042",
        "9780000000059",
        "9780000000066",
        "9780000000073"
    ]

    assert binary_search(
        isbns,
        "9780000000066"
    ) == (5, 2)


def test_binary_search_not_found():
    isbns = [
        "9780000000011",
        "9780000000028",
        "9780000000035",
        "9780000000042",
        "9780000000059",
        "9780000000066",
        "9780000000073"
    ]

    assert binary_search(
        isbns,
        "9780000000050"
    ) == (-1, 3)


def test_binary_search_empty_list():
    assert binary_search(
        [],
        "9780000000011"
    ) == (-1, 0)


def test_binary_search_one_element():
    assert binary_search(
        ["9780000000011"],
        "9780000000011"
    ) == (0, 1)


# Sorting tests

def test_bubble_sort():
    assert bubble_sort(
        [5, 2, 4, 1],
        show_passes=False
    ) == [1, 2, 4, 5]


def test_insertion_sort():
    assert insertion_sort(
        [5, 2, 4, 1],
        show_passes=False
    ) == [1, 2, 4, 5]


def test_selection_sort():
    assert selection_sort(
        [5, 2, 4, 1],
        show_passes=False
    ) == [1, 2, 4, 5]


def test_sort_empty_list():
    assert bubble_sort([], show_passes=False) == []
    assert insertion_sort([], show_passes=False) == []
    assert selection_sort([], show_passes=False) == []


def test_sort_single_element():
    assert bubble_sort([5], show_passes=False) == [5]
    assert insertion_sort([5], show_passes=False) == [5]
    assert selection_sort([5], show_passes=False) == [5]


# Catalogue sorting tests

def test_top_level_category():
    books = sample_books()

    assert top_level_category(books[2]) == "Technology"
    assert top_level_category(books[3]) == "Technology"


def test_catalogue_sort():
    books = sample_books()

    sorted_books = catalogue_sort(books)

    assert [
        book.title for book in sorted_books
    ] == [
        "Wings of Fire",
        "The Alchemist",
        "Python Crash Course",
        "Clean Code"
    ]