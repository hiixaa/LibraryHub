
from storage.database import get_connection


def search_unsafe(search_term):
    """Intentionally vulnerable SQL query."""
    query = f"""
        SELECT isbn, title
        FROM items
        WHERE title = '{search_term}'
    """

    with get_connection() as connection:
        return connection.execute(query).fetchall()


def search_safe(search_term):
    """Secure parameterized SQL query."""
    query = """
        SELECT isbn, title
        FROM items
        WHERE title = ?
    """

    with get_connection() as connection:
        return connection.execute(query, (search_term,)).fetchall()


if __name__ == "__main__":
    normal_input = "Python Crash Course"
    malicious_input = "' OR '1'='1"

    print("NORMAL SEARCH")
    print("Unsafe:", search_unsafe(normal_input))
    print("Safe:", search_safe(normal_input))

    print("\nSQL INJECTION TEST")
    print("Malicious input:", malicious_input)

    unsafe_results = search_unsafe(malicious_input)
    safe_results = search_safe(malicious_input)

    print("Unsafe result count:", len(unsafe_results))
    print("Safe result count:", len(safe_results))
