
from abc import ABC, abstractmethod


class LibraryItem(ABC):

    def __init__(self, isbn, title, authors, category,
                 pages, price, total_copies, parent_category=None):

        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.category = category
        self.parent_category = parent_category
        self.pages = pages
        self.price = price
        self.total_copies = total_copies
        self.available_copies = total_copies

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, value):
        value = str(value)

        if len(value) != 13 or not value.isdigit():
            raise ValueError("ISBN must be exactly 13 digits.")

        self._isbn = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title cannot be blank.")

        self._title = value.strip()

    @property
    def total_copies(self):
        return self._total_copies

    @total_copies.setter
    def total_copies(self, value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("Copies cannot be negative.")

        self._total_copies = value

    @abstractmethod
    def loan_period(self, member):
        pass

    @property
    @abstractmethod
    def borrowable(self):
        pass

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"isbn={self.isbn!r}, title={self.title!r})"
        )


class Book(LibraryItem):

    def loan_period(self, member):
        return member.loan_period()

    @property
    def borrowable(self):
        return True


class Magazine(LibraryItem):

    def loan_period(self, member):
        return 7

    @property
    def borrowable(self):
        return True


class ReferenceItem(LibraryItem):

    def loan_period(self, member):
        return 0

    @property
    def borrowable(self):
        return False
