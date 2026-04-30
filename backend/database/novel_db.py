from typing import Optional
from sqlite3 import Connection

# TODO: "with conn:" auto commits and rolls back, but it doesnt raise exeption. Currently front end fails, but no message
# Consider adding error handling to raise exceptions on failure, or at least log them
def _row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"]
    }

def create_novel(conn: Connection, title: str) -> int | None:
    with conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO novels (title) VALUES (?)", (title,))
        return cursor.lastrowid

def get_novel(conn: Connection, novel_id: int) -> Optional[dict]:
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM novels WHERE id = ?", (novel_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return _row_to_dict(row)

def get_novels(conn: Connection) -> list[dict]:
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM novels")
        return [_row_to_dict(row) for row in cursor.fetchall()]

def update_novel(conn: Connection, novel_id: int, title: str) -> bool:
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE novels SET title = ? WHERE id = ?",
            (title, novel_id)
        )
        return cursor.rowcount > 0

def delete_novel(conn: Connection, novel_id: int) -> bool:
    with conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM novels WHERE id = ?", (novel_id,))
        conn.commit()
        return cursor.rowcount > 0