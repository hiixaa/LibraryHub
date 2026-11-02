from pathlib import Path

from dsa.hashing import import_books


def main():
    project_folder = Path(__file__).resolve().parent

    csv_path = project_folder / "books_with_duplicate.csv"

    if not csv_path.exists():
        print("Error: books_with_duplicate.csv was not found.")
        return

    imported_items = import_books(csv_path)

    print("\nSuccessfully imported titles:")

    for item in imported_items:
        print(item.title)


if __name__ == "__main__":
    main()