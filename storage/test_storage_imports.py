from storage.database import get_connection
from storage.item_storage import ItemStorage
from storage.member_storage import MemberStorage
from storage.loan_storage import LoanStorage


def main():
    with get_connection() as connection:
        print("Database connection: SUCCESS")

    item_storage = ItemStorage()
    member_storage = MemberStorage()
    loan_storage = LoanStorage()

    print("ItemStorage:", len(item_storage.get_all()), "items")
    print("MemberStorage:", len(member_storage.get_all()), "members")
    print("LoanStorage:", len(loan_storage.get_all()), "loans")

    print("\nAll storage classes imported successfully!")


if __name__ == "__main__":
    main()