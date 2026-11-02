
import sqlite3
from pathlib import Path
from contextlib import contextmanager


# Project root directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# SQLite database path
DB_PATH = PROJECT_DIR / "libraryhub.db"


def _ensure_compatibility(connection):
    """
    Apply small, additive database changes required by the application.
    """

    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(loans)")
    }

    # Store how many times a loan has been renewed.
    if "renewal_count" not in columns:
        connection.execute(
            """
            ALTER TABLE loans
            ADD COLUMN renewal_count INTEGER NOT NULL DEFAULT 0
            """
        )


@contextmanager
def get_connection():
    """
    Open a database connection.

    Automatically commits when operations succeed
    and rolls back when an exception occurs.
    """

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    # Enable foreign key constraints.
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        _ensure_compatibility(connection)

        yield connection

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
