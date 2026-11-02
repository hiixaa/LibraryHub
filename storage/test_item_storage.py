
from storage.item_storage import ItemStorage


def test_item_storage():
    storage = ItemStorage()

    # Test 1: Fetch all items
    print("\nTEST 1: GET ALL ITEMS")
    items = storage.get_all()

    print("Total items:", len(items))

    for item in items:
        print(item[1], "| ISBN:", item[0])

    # Test 2: Fetch one item
    print("\nTEST 2: GET ITEM BY ISBN")
    item = storage.get_by_isbn("9780000000011")

    print("Item found:", item)

    # Test 3: Fetch authors
    print("\nTEST 3: GET AUTHORS")
    authors = storage.get_authors("9780000000011")

    print("Authors:", authors)

    # Basic verification
    assert len(items) == 7
    assert item is not None
    assert item[1] == "Wings of Fire"
    assert len(authors) == 2

    print("\nAll ItemStorage tests passed!")


if __name__ == "__main__":
    test_item_storage()
