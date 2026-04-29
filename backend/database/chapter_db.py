from typing import Optional
from sqlite3 import Connection
import os
import hashlib

BASE_DIR = "data/raw"

def _row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "novel_id": row["novel_id"],
        "chapter_number": row["chapter_number"],
        "title": row["title"],
        "raw_file_path": row["raw_file_path"],
        "annotated_file_path": row["annotated_file_path"],
        "hash": row["hash"]
    }

def create_chapter(conn: Connection, 
                   novel_id: int, 
                   chapter_number: int, 
                   title: str) -> int | None:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chapters (novel_id, chapter_number, title) VALUES (?, ?, ?)",
        (novel_id, chapter_number, title)
    )
    conn.commit()
    return cursor.lastrowid

def get_chapter(conn: Connection, 
                chapter_id: int | None = None, 
                novel_id: int | None = None, 
                chapter_number: int | None = None) -> Optional[dict]:
    cursor = conn.cursor()
    if chapter_id is not None:
        cursor.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,))
    elif novel_id is not None and chapter_number is not None:
        cursor.execute("SELECT * FROM chapters WHERE novel_id = ? AND chapter_number = ?",(novel_id, chapter_number))
    else:
        return None
    row = cursor.fetchone()
    return _row_to_dict(row) if row else None

def get_chapters_by_novel(conn: Connection, novel_id: int) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chapters WHERE novel_id = ?", (novel_id,))
    rows = cursor.fetchall()
    return [_row_to_dict(row) for row in rows]

def update_chapter(conn: Connection, 
                   chapter_id: int | None = None, 
                   chapter_number: int | None = None, 
                   title: str | None = None) -> bool:
    cursor = conn.cursor()

    updates = []
    params = []

    if chapter_number is not None:
        updates.append("chapter_number = ?")
        params.append(chapter_number)
    
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    
    if updates:
        params.append(chapter_id)
        query = f"UPDATE chapters SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)

    conn.commit()

    return cursor.rowcount > 0

def save_chapter_content(conn: Connection, 
                           chapter_id: int, 
                           content: str,
                           base_dir: str|None = None) -> str:
    
    if base_dir is None:
        base_dir = BASE_DIR
    
    os.makedirs(base_dir, exist_ok=True)

    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    file_path = os.path.join(base_dir, f"{chapter_id}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE chapters
        SET raw_file_path = ?, hash = ?
        WHERE id = ?
        """,
        (file_path, content_hash, chapter_id)
    )
    conn.commit()

    return file_path, content_hash #TODO: content_hash not yet used

def load_chapter_content(conn: Connection, chapter_id: int) -> Optional[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT raw_file_path FROM chapters WHERE id = ?", (chapter_id,))
    row = cursor.fetchone()
    if not row or not row["raw_file_path"]:
        return None

    with open(row["raw_file_path"], "r", encoding="utf-8") as f:
        return f.read()

def delete_chapter(conn: Connection, chapter_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
    conn.commit()
    return cursor.rowcount > 0
