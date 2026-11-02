from storage.object_mapper import ObjectMapper


def test_object_mapper():
    mapper = ObjectMapper()

    print("\nTEST 1: LOAD ITEMS")
    items = mapper.load_items()

    print("Total items:", len(items))

    for item in items.values():
        print(
            item.title,
            "|",
            type(item).__name__,
            "| Available:",
            item.available_copies
        )

    print("\nTEST 2: LOAD MEMBERS")
    members = mapper.load_members()

    print("Total members:", len(members))

    for member in members.values():
        print(
            member.name,
            "|",
            type(member).__name__
        )

    print("\nTEST 3: LOAD LOANS")
    loans = mapper.load_loans(members, items)

    print("Total loans:", len(loans))

    for loan in loans:
        print(
            loan.loan_id,
            "|",
            loan.member.name,
            "|",
            loan.item.title,
            "| Returned:",
            loan.is_returned
        )

    print("\nAll ObjectMapper tests passed!")


if __name__ == "__main__":
    test_object_mapper()