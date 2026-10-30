from library import Library
from items import ReferenceItem
from datetime import date

def display_menu():
    print("\n=== LibraryHub Mini ===")
    print("1. List catalogue")
    print("2. Search by title or author")
    print("3. Borrow")
    print("4. Return")
    print("5. Renew")
    print("6. Join waiting list")
    print("7. Member loans")
    print("8. Overdue report")
    print("0. Exit")

def show_catalogue(library):
    items = library.list_items()

    print("\nISBN             TITLE                     TYPE        AVAILABLE")

    for item in items:
        if item.borrowable:
            availability = f"{item.available_copies} of {item.total_copies}"
        else:
            availability = "Not borrowable"

        item_type = (
            "Reference" if isinstance(item, ReferenceItem)
            else type(item).__name__
        )

        print(
            f"{item.isbn}  "
            f"{item.title:<25} "
            f"{item_type:<11} "
            f"{availability}"
        )


def search_catalogue(library):
    search_term = input("Enter title or author: ").strip()

    if not search_term:
        print("Search term cannot be empty.")
        return

    results = library.search_items(search_term)

    if not results:
        print("No matching items found.")
        return

    print("\nSearch results:")

    for item in results:
        if item.borrowable:
            availability = f"{item.available_copies} of {item.total_copies}"
        else:
            availability = "not borrowable"

        item_type = (
            "Reference" if isinstance(item, ReferenceItem)
            else type(item).__name__
        )

        print(
            f"{item.isbn}  "
            f"{item.title:<25} "
            f"{item_type:<11} "
            f"{availability}"
        )


def borrow_item(library):
    member_id = input("Enter Member ID: ").strip()
    isbn = input("Enter ISBN: ").strip()

    try:
        loan = library.borrow(isbn, member_id)
        print("\nItem borrowed successfully!")
        print(f"Loan ID: {loan.loan_id}")
        print(f"Title: {loan.item.title}")
        print(f"Due date: {loan.due_date}")

    except Exception as error:
        print(f"ERROR: {error}")


def return_book(library):
    member_id = input("Enter Member ID: ").strip()
    isbn = input("Enter ISBN: ").strip()

    try:
        loan = library.return_item(isbn, member_id)

        print("\nItem returned successfully!")
        print(f"Loan ID: {loan.loan_id}")
        print(f"Title: {loan.item.title}")

        if library.last_notified_member:
            print(
                f"Next member notified: "
                f"{library.last_notified_member.name}"
            )

    except Exception as error:
        print(f"ERROR: {error}")


def renew_book(library):
    member_id = input("Enter Member ID: ").strip()
    isbn = input("Enter ISBN: ").strip()

    try:
        loan = library.renew(isbn, member_id)

        print("\nItem renewed successfully!")
        print(f"Loan ID: {loan.loan_id}")
        print(f"Title: {loan.item.title}")
        print(f"New due date: {loan.due_date}")
        print(f"Renewal count: {loan.renewal_count}")

    except Exception as error:
        print(f"ERROR: {error}")


def join_waiting_list(library):
    member_id = input("Enter Member ID: ").strip()
    isbn = input("Enter ISBN: ").strip()

    try:
        position = library.reserve(isbn, member_id)

        print("\nSuccessfully joined the waiting list!")
        print(f"Waiting list position: {position}")

    except Exception as error:
        print(f"ERROR: {error}")


def show_member_loans(library):
    member_id = input("Enter Member ID: ").strip()

    try:
        member = library.get_member(member_id)
        loans = library.member_loans(member_id)

        print(f"\nLoans for {member.name}")
        print("LOAN   TITLE                     ISSUED       DUE          STATUS")

        today = date(2026, 10, 12)
        for loan in loans:
            status = (
                f"OVERDUE ({(today - loan.due_date).days} days)"
                if loan.is_overdue(today)
                else "On loan"
            )

            print(
                f"{loan.loan_id:<6} "
                f"{loan.item.title:<25} "
                f"{loan.borrowed_date} "
                f"{loan.due_date} "
                f"{status}"
            )

        print(f"\nActive loans: {len(loans)} of {member.max_items}")
        print(f"Unpaid fines: ₹{member.unpaid_fines:.0f}")

    except Exception as error:
        print(f"ERROR: {error}")

def show_overdue_report(library):
    today = date(2026, 10, 12)

    overdue_loans = library.overdue_report(today)

    print("\nOVERDUE REPORT")
    print("-" * 75)

    if not overdue_loans:
        print("No overdue loans.")
        return

    total_fines = 0

    for loan in overdue_loans:
        overdue_days = (today - loan.due_date).days
        fine = loan.calculate_fine(today)
        total_fines += fine

        print(
            f"{loan.loan_id:<8} "
            f"{loan.member.name:<18} "
            f"{loan.item.title:<25} "
            f"Due: {loan.due_date} "
            f"Overdue: {overdue_days} days "
            f"Fine: ₹{fine}"
        )

    print("-" * 75)
    print(f"Total overdue loans: {len(overdue_loans)}")
    print(f"Total fines: ₹{total_fines}")


def main():
    library = Library()
    library.load_data()

    while True:
        display_menu()

        try:
            choice = int(input("> "))

            if choice < 0 or choice > 8:
                print("Please enter a number from 0 to 8.")
                continue

            if choice == 0:
                print("Thank you for using LibraryHub Mini!")
                break

            if choice == 1:
                show_catalogue(library)
            elif choice == 2:
                search_catalogue(library)
            elif choice == 3:
                borrow_item(library)
            elif choice == 4:
                return_book(library)
            elif choice == 5:
                renew_book(library)
            elif choice == 6:
                join_waiting_list(library)
            elif choice == 7:
                show_member_loans(library)
            elif choice == 8:
                show_overdue_report(library)
            else:
                print("This option will be implemented next.")
        except ValueError:
            print("Please enter a number from 0 to 8.")

        finally:
            pass


if __name__ == "__main__":
    main()
