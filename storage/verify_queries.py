
import sqlite3
from pathlib import Path

# Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_DIR / "libraryhub.db"
QUERIES_PATH = PROJECT_DIR / "queries.sql"


def verify_queries():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    sql_content = QUERIES_PATH.read_text(encoding="utf-8")

    statement = ""
    query_number = 0

    print("LIBRARYHUB - SQL QUERY VERIFICATION")
    print("=" * 50)

    for line in sql_content.splitlines():
        statement += line + "\n"

        if sqlite3.complete_statement(statement):
            sql = statement.strip()
            statement = ""

            if not sql or not any(
                part.strip() and not part.strip().startswith("--")
                for part in sql.splitlines()
            ):
                continue

            try:
                cursor.execute(sql)

                if cursor.description:
                    query_number += 1
                    rows = cursor.fetchall()

                    print(f"\nQ{query_number}")
                    print("-" * 40)

                    if rows:
                        for row in rows:
                            print(row)
                    else:
                        print("No records found.")

            except sqlite3.Error as error:
                print(f"\nSQL ERROR: {error}")
                print("Check the corresponding query in queries.sql.")
                break

    connection.close()

    print("\n" + "=" * 50)
    print(f"Total queries executed: {query_number}")


if __name__ == "__main__":
    verify_queries()
