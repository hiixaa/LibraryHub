
from storage.loan_storage import LoanStorage


def test_loan_storage():
    storage = LoanStorage()

    # Test 1: Fetch all loans
    print("\nTEST 1: GET ALL LOANS")

    loans = storage.get_all()

    print("Total loans:", len(loans))

    for loan in loans:
        print(
            loan[0],
            "|",
            loan[2],
            "|",
            loan[4],
            "| Returned:",
            loan[7]
        )

    # Test 2: Fetch loan by ID
    print("\nTEST 2: GET LOAN BY ID")

    loan = storage.get_by_id("L001")
    print("Loan found:", loan)

    # Test 3: Fetch active loans
    print("\nTEST 3: GET ACTIVE LOANS")

    active_loans = storage.get_active_loans()

    print("Active loans:", len(active_loans))

    for active_loan in active_loans:
        print(active_loan)

    # Verification
    assert len(loans) == 10
    assert loan is not None
    assert loan[0] == "L001"
    assert len(active_loans) == 3

    print("\nAll LoanStorage tests passed!")


if __name__ == "__main__":
    test_loan_storage()
