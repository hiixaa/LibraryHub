
import sqlite3
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Database and schema file paths
DB_PATH = PROJECT_ROOT / "libraryhub.db"
SCHEMA_PATH = PROJECT_ROOT / "schema.sql"


def initialise_database():
    connection = sqlite3.connect(DB_PATH)

    try:
        # Enable foreign key enforcement for this connection
        connection.execute("PRAGMA foreign_keys = ON")

        # Read the SQL schema
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            schema = file.read()

        # Execute all CREATE TABLE statements
        connection.executescript(schema)
        connection.commit()

        print("Database initialised successfully!")
        print(f"Database location: {DB_PATH}")

        # Display all created tables
        cursor = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        print("\nTables created:")
        for row in cursor.fetchall():
            print("-", row[0])

    except sqlite3.Error as error:
        connection.rollback()
        print("Database error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    initialise_database()
