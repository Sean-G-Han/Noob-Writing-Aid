from typing import Optional
from sqlite3 import Connection
from .cursor_singleton import CursorSingleton

def _row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"]
    }

def create_novel(conn: Connection, title: str) -> int | None:
    cursor = CursorSingleton.get_instance(conn)
    cursor.execute("INSERT INTO novels (title) VALUES (?)", (title,))
    conn.commit()
    return cursor.lastrowid

def get_novel(conn: Connection, novel_id: int) -> Optional[dict]:
    cursor = CursorSingleton.get_instance(conn)
    cursor.execute("SELECT * FROM novels WHERE id = ?", (novel_id,))
    row = cursor.fetchone()
    if not row:
        return None
    return _row_to_dict(row)

def get_novels(conn: Connection) -> list[dict]:
    cursor = CursorSingleton.get_instance(conn)
    cursor.execute("SELECT * FROM novels")
    return [_row_to_dict(row) for row in cursor.fetchall()]

def update_novel(conn: Connection, novel_id: int, title: str) -> bool:
    cursor = CursorSingleton.get_instance(conn)
    cursor.execute(
        "UPDATE novels SET title = ? WHERE id = ?",
        (title, novel_id)
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_novel(conn: Connection, novel_id: int) -> bool:
    cursor = CursorSingleton.get_instance(conn)
    cursor.execute("DELETE FROM novels WHERE id = ?", (novel_id,))
    conn.commit()
    return cursor.rowcount > 0