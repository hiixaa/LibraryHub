import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Read starter CSV files
with open(BASE_DIR / "books.csv", newline="", encoding="utf-8") as file:
    books = {
        row["isbn"]: row
        for row in csv.DictReader(file)
    }

with open(BASE_DIR / "members.csv", newline="", encoding="utf-8") as file:
    members = {
        row["member_id"]: row
        for row in csv.DictReader(file)
    }

with open(BASE_DIR / "loans.csv", newline="", encoding="utf-8") as file:
    loans = list(csv.DictReader(file))

with open(BASE_DIR / "fines.csv", newline="", encoding="utf-8") as file:
    fines = {
        row["loan_id"]: row
        for row in csv.DictReader(file)
    }


# Required flat-file columns
fieldnames = [
    "loan_id",
    "member_name",
    "email",
    "membership_type",
    "item_title",
    "authors",
    "isbn",
    "category",
    "parent_category",
    "pages",
    "price",
    "issue_date",
    "due_date",
    "return_date",
    "fine",
    "fine_paid",
]

# Combine the data
flat_rows = []

for loan in loans:
    member = members[loan["member_id"]]
    item = books[loan["isbn"]]

    fine = fines.get(loan["loan_id"], {})

    flat_rows.append({
        "loan_id": loan["loan_id"],
        "member_name": member["name"],
        "email": member["email"],
        "membership_type": member["membership_type"],
        "item_title": item["title"],
        "authors": item["authors"],
        "isbn": item["isbn"],
        "category": item["category"],
        "parent_category": item["parent_category"],
        "pages": item["pages"],
        "price": item["price"],
        "issue_date": loan["issue_date"],
        "due_date": loan["due_date"],
        "return_date": loan["return_date"],
        "fine": fine.get("amount", ""),
        "fine_paid": fine.get("paid", ""),
    })


# Write the combined flat file
output_path = BASE_DIR / "library_flat.csv"

with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(flat_rows)

print("Flat file created successfully!")
print("Total rows:", len(flat_rows))
print("Output:", output_path.name)