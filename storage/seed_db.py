
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "libraryhub.db"
SEED_PATH = PROJECT_ROOT / "seed.sql"


def seed_database():
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        with open(SEED_PATH, "r", encoding="utf-8") as file:
            seed_sql = file.read()

        connection.executescript(seed_sql)
        connection.commit()

        print("Starter data inserted successfully!")

        tables = [
            "membership_types",
            "members",
            "categories",
            "items",
            "authors",
            "item_authors",
            "loans",
            "fines",
            "reservations",
            "audit_log"
        ]

        print("\nRecord counts:")
        for table in tables:
            cursor = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            )
            count = cursor.fetchone()[0]
            print(f"{table}: {count}")

    except sqlite3.Error as error:
        connection.rollback()
        print("Database error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    seed_database()
