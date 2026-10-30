import pytest

from errors import (
    LibraryError,
    ItemNotAvailableError,
    MemberNotFoundError,
)


def test_item_not_available_error():
    with pytest.raises(ItemNotAvailableError):
        raise ItemNotAvailableError("No copies available.")


def test_member_not_found_error():
    with pytest.raises(MemberNotFoundError):
        raise MemberNotFoundError("Member not found.")


def test_custom_errors_inherit_from_library_error():
    assert issubclass(ItemNotAvailableError, LibraryError)
    assert issubclass(MemberNotFoundError, LibraryError)