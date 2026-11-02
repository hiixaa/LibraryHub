import csv
from collections import defaultdict

from items import Book, Magazine, ReferenceItem


def import_books(csv_path):
    imported_items = []
    used_isbns = set()
    isbn_titles = {}

    total_rows = 0
    duplicate_count = 0

    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for line_number, row in enumerate(reader, start=2):
            total_rows += 1
            isbn = row["isbn"].strip()

            if isbn in used_isbns:
                duplicate_count += 1

                print(
                    f"Line {line_number}: duplicate ISBN {isbn} "
                    f"(already used by '{isbn_titles[isbn]}'), skipped."
                )
                continue

            authors = [
                author.strip()
                for author in row["authors"].split(";")
                if author.strip()
            ]

            item_type = row["item_type"].strip()

            item_classes = {
                "Book": Book,
                "Magazine": Magazine,
                "Reference": ReferenceItem
            }

            if item_type not in item_classes:
                raise ValueError(
                    f"Unsupported item type '{item_type}' "
                    f"at line {line_number}."
                )

            item_class = item_classes[item_type]

            item = item_class(
                isbn,
                row["title"],
                authors,
                row["category"],
                int(row["pages"]),
                float(row["price"]),
                int(row["total_copies"]),
                row.get("parent_category") or None
            )

            used_isbns.add(isbn)
            isbn_titles[isbn] = item.title
            imported_items.append(item)

    print(
        f"Imported {total_rows} rows: "
        f"{len(imported_items)} added, "
        f"{duplicate_count} duplicate skipped."
    )

    return imported_items


def group_by_author(items):
    author_groups = defaultdict(list)

    for item in items:
        for author in item.authors:
            author_groups[author.strip()].append(item.title)

    return {
        author: sorted(titles, key=str.casefold)
        for author, titles in sorted(
            author_groups.items(),
            key=lambda entry: entry[0].casefold()
        )
    }


def most_borrowed(loans_csv, items, limit=3):
    isbn_to_title = {
        item.isbn: item.title
        for item in items
    }

    frequencies = {}

    with open(loans_csv, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            isbn = row["isbn"].strip()

            if isbn in isbn_to_title:
                frequencies[isbn] = frequencies.get(isbn, 0) + 1

    results = [
        (isbn_to_title[isbn], count)
        for isbn, count in frequencies.items()
    ]

    results.sort(
        key=lambda entry: (-entry[1], entry[0].casefold())
    )

    return results[:limit]


def reading_challenge(items, target_pages):
    seen_pages = {}

    for item in items:
        if not item.borrowable:
            continue

        required_pages = target_pages - item.pages

        if required_pages in seen_pages:
            return seen_pages[required_pages], item

        if item.pages not in seen_pages:
            seen_pages[item.pages] = item

    return None