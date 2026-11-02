
import sqlite3
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_library_database(tmp_path, monkeypatch):
    """
    Give every pytest test its own temporary SQLite database.
    The actual libraryhub.db remains untouched.
    """

    from storage import database

    project_dir = Path(__file__).resolve().parent

    test_db_path = tmp_path / "libraryhub_test.db"

    # Redirect all storage database connections.
    monkeypatch.setattr(database, "DB_PATH", test_db_path)

    schema_path = project_dir / "schema.sql"
    seed_path = project_dir / "seed.sql"

    # Load the schema and original sample data.
    schema_sql = schema_path.read_text(encoding="utf-8")
    seed_sql = seed_path.read_text(encoding="utf-8")

    with sqlite3.connect(test_db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema_sql)
        connection.executescript(seed_sql)

    yield test_db_path
