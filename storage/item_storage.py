
from storage.database import get_connection


class ItemStorage:

    def get_all(self):
        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    i.isbn,
                    i.title,
                    i.item_type,
                    c.category_name,
                    i.pages,
                    i.price,
                    i.total_copies,
                    parent.category_name
                FROM items i
                INNER JOIN categories c
                    ON i.category_id = c.category_id
                LEFT JOIN categories parent
                    ON c.parent_category_id = parent.category_id
                ORDER BY i.title
            """)

            return cursor.fetchall()

    def get_by_isbn(self, isbn):
        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    i.isbn,
                    i.title,
                    i.item_type,
                    c.category_name,
                    i.pages,
                    i.price,
                    i.total_copies,
                    parent.category_name
                FROM items i
                INNER JOIN categories c
                    ON i.category_id = c.category_id
                LEFT JOIN categories parent
                    ON c.parent_category_id = parent.category_id
                WHERE i.isbn = ?
            """, (isbn,))

            return cursor.fetchone()

    def get_authors(self, isbn):
        """Fetch all authors associated with an item."""

        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT a.author_name
                FROM authors a
                INNER JOIN item_authors ia
                    ON a.author_id = ia.author_id
                WHERE ia.isbn = ?
                ORDER BY a.author_name
            """, (isbn,))

            return [row[0] for row in cursor.fetchall()]

    def add(self, item):
        """Insert a new item and its authors into the database."""

        with get_connection() as connection:
            cursor = connection.cursor()

            # Find or create category
            cursor.execute("""
                SELECT category_id
                FROM categories
                WHERE category_name = ?
            """, (item["category"],))

            category = cursor.fetchone()

            if category:
                category_id = category["category_id"]
            else:
                cursor.execute("""
                    INSERT INTO categories (category_name)
                    VALUES (?)
                """, (item["category"],))

                category_id = cursor.lastrowid

            # Insert item
            cursor.execute("""
                INSERT INTO items (
                    isbn,
                    title,
                    item_type,
                    category_id,
                    pages,
                    price,
                    total_copies
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item["isbn"],
                item["title"],
                item["item_type"],
                category_id,
                item["pages"],
                item["price"],
                item["total_copies"]
            ))

            # Insert authors and link them to the item
            for author_name in item["authors"]:
                author_name = author_name.strip()

                if not author_name:
                    continue

                cursor.execute("""
                    INSERT OR IGNORE INTO authors (author_name)
                    VALUES (?)
                """, (author_name,))

                cursor.execute("""
                    SELECT author_id
                    FROM authors
                    WHERE author_name = ?
                """, (author_name,))

                author_id = cursor.fetchone()["author_id"]

                cursor.execute("""
                    INSERT INTO item_authors (isbn, author_id)
                    VALUES (?, ?)
                """, (item["isbn"], author_id))
