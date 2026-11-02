
from storage.member_storage import MemberStorage


def test_member_storage():
    storage = MemberStorage()

    # Test 1: Fetch all members
    print("\nTEST 1: GET ALL MEMBERS")

    members = storage.get_all()

    print("Total members:", len(members))

    for member in members:
        print(
            member[0],
            "|",
            member[1],
            "|",
            member[3],
            "| Loan limit:",
            member[4]
        )

    # Test 2: Fetch member by ID
    print("\nTEST 2: GET MEMBER BY ID")

    member = storage.get_by_id("M001")

    print("Member found:", member)

    # Test 3: Fetch member by email
    print("\nTEST 3: GET MEMBER BY EMAIL")

    member_email = storage.get_by_email("asha@example.com")

    print("Member found:", member_email)

    # Verification
    assert len(members) == 5
    assert member is not None
    assert member[1] == "Asha Raman"
    assert member_email is not None
    assert member_email[0] == "M001"

    print("\nAll MemberStorage tests passed!")


if __name__ == "__main__":
    test_member_storage()
