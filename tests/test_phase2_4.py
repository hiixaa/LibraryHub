from datetime import date

from library import Library
from items import Book
from members import StudentMember


def create_library():
    library = Library()

    item = Book(
        "9780000000099",
        "Test Book",
        ["Test Author"],
        "Fiction",
        200,
        300,
        1,
    )

    member1 = StudentMember("M101", "Asha", "asha@test.com")
    member2 = StudentMember("M102", "Sneha", "sneha@test.com")
    member3 = StudentMember("M103", "Rahul", "rahul@test.com")

    library.add_item(item)
    library.add_member(member1)
    library.add_member(member2)
    library.add_member(member3)

    return library


def test_undo_borrow():
    library = create_library()

    loan = library.borrow(
        "9780000000099",
        "M101",
        date(2026, 10, 12),
    )

    assert library.get_item("9780000000099").available_copies == 0

    result = library.undo()

    assert result["action"] == "borrow"
    assert loan not in library.loans
    assert library.get_item("9780000000099").available_copies == 1
    assert loan not in library.get_borrow_history()


def test_undo_return():
    library = create_library()

    loan = library.borrow(
        "9780000000099",
        "M101",
        date(2026, 10, 12),
    )

    library.return_item(
        "9780000000099",
        "M101",
        date(2026, 10, 15),
    )

    assert loan.is_returned

    result = library.undo()

    assert result["action"] == "return"
    assert not loan.is_returned
    assert library.get_item("9780000000099").available_copies == 0


def test_undo_empty_stack():
    library = create_library()

    assert library.undo() is None


def test_waiting_list_fifo():
    library = create_library()

    library.borrow(
        "9780000000099",
        "M101",
        date(2026, 10, 12),
    )

    library.reserve("9780000000099", "M102")
    library.reserve("9780000000099", "M103")

    waiting = library.get_waiting_list("9780000000099")

    assert [member.member_id for member in waiting] == ["M102", "M103"]


def test_return_serves_first_waiting_member():
    library = create_library()

    library.borrow(
        "9780000000099",
        "M101",
        date(2026, 10, 12),
    )

    library.reserve("9780000000099", "M102")
    library.reserve("9780000000099", "M103")

    library.return_item(
        "9780000000099",
        "M101",
        date(2026, 10, 15),
    )

    assert library.last_notified_member.member_id == "M102"

    waiting = library.get_waiting_list("9780000000099")

    assert [member.member_id for member in waiting] == ["M103"]


def test_undo_return_restores_waiting_queue():
    library = create_library()

    library.borrow(
        "9780000000099",
        "M101",
        date(2026, 10, 12),
    )

    library.reserve("9780000000099", "M102")
    library.reserve("9780000000099", "M103")

    library.return_item("9780000000099", "M101")

    library.undo()

    waiting = library.get_waiting_list("9780000000099")

    assert [member.member_id for member in waiting] == ["M102", "M103"]
    assert library.last_notified_member is None


def test_borrow_history_newest_first():
    library = create_library()

    first = library.borrow(
        "9780000000099",
        "M101",
        date(2026, 10, 12),
    )

    library.undo()

    second = library.borrow(
        "9780000000099",
        "M102",
        date(2026, 10, 13),
    )

    history = library.get_borrow_history()

    assert history[0] == second
    assert first not in history