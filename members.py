from abc import ABC, abstractmethod


class Member(ABC):

    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.unpaid_fines = 0

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or "@" not in value:
            raise ValueError("Email must contain @.")

        self._email = value

    @property
    @abstractmethod
    def max_items(self):
        pass

    @abstractmethod
    def loan_period(self):
        pass

    @property
    @abstractmethod
    def daily_fine_rate(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.member_id})"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"member_id={self.member_id!r}, name={self.name!r})"
        )


class StudentMember(Member):

    @property
    def max_items(self):
        return 3

    def loan_period(self):
        return 14

    @property
    def daily_fine_rate(self):
        return 2


class RegularMember(Member):

    @property
    def max_items(self):
        return 5

    def loan_period(self):
        return 21

    @property
    def daily_fine_rate(self):
        return 5


class PremiumMember(Member):

    @property
    def max_items(self):
        return 10

    def loan_period(self):
        return 30

    @property
    def daily_fine_rate(self):
        return 3
