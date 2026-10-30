
class LibraryError(Exception):
    """Base exception for LibraryHub."""


class InvalidISBNError(LibraryError):
    """Raised when an ISBN is invalid."""


class ItemNotFoundError(LibraryError):
    """Raised when an item does not exist."""


class MemberNotFoundError(LibraryError):
    """Raised when a member does not exist."""


class ItemNotBorrowableError(LibraryError):
    """Raised when an item cannot be borrowed (R1)."""


class UnpaidFinesError(LibraryError):
    """Raised when unpaid fines exceed ₹100 (R4)."""


class BorrowLimitExceededError(LibraryError):
    """Raised when a member reaches their borrowing limit (R3)."""


class DuplicateLoanError(LibraryError):
    """Raised when a member already holds the same title (R8)."""


class ItemNotAvailableError(LibraryError):
    """Raised when no copy is available (R7)."""


class RenewalNotAllowedError(LibraryError):
    """Raised when renewal is prohibited (R2 or R6)."""


class LoanNotFoundError(LibraryError):
    """Raised when an active loan cannot be found."""


class ReservationError(LibraryError):
    """Raised when a reservation cannot be made."""
