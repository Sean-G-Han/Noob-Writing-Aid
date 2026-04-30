from typing import Optional
from sqlite3 import Connection
import sqlite3
from database.exceptions import DBError
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

OFFSET = 1000000

def _shift_down(cursor, novel_id: int, start: int, end: int):
    cursor.execute("""
        UPDATE chapters
        SET chapter_number = chapter_number + ?
        WHERE novel_id = ?
          AND chapter_number > ?
          AND chapter_number <= ?
    """, (OFFSET, novel_id, start, end))

    cursor.execute("""
        UPDATE chapters
        SET chapter_number = chapter_number - (? + 1)
        WHERE novel_id = ?
          AND chapter_number > ?
          AND chapter_number <= ?
    """, (OFFSET, novel_id, start + OFFSET, end + OFFSET))

def create_chapter(conn: Connection, 
                   novel_id: int, 
                   chapter_number: int, 
                   title: str) -> int | None:
    try:
        with conn:
            cursor = conn.cursor()

            # YH Notes: Hacky way to shift chapter numbers down to make room for the new chapter.
            # This is necessary because chapter numbers are unique based on schema
            # SQLite doesn't support UPDATE with ordering so doing UPDATE + 1 will cause conflicts
            # This solution sends only 3 requests to the database, regardless of how many chapters need to be shifted
            _shift_down(cursor, novel_id, chapter_number, OFFSET)

            cursor.execute(
                "INSERT INTO chapters (novel_id, chapter_number, title) VALUES (?, ?, ?)", 
                (novel_id, chapter_number, title)
            )
            return cursor.lastrowid
    except sqlite3.Error as e:
        raise DBError(f"Failed to create chapter: {str(e)}") from e

def append_chapter(conn: Connection, 
                   novel_id: int, 
                   title: str) -> int | None:
    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COALESCE(MAX(chapter_number), 0) + 1
                FROM chapters
                WHERE novel_id = ?
            """, (novel_id,))
            
            next_number = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO chapters (novel_id, chapter_number, title) VALUES (?, ?, ?)", 
                (novel_id, next_number, title)
            )
            

            return cursor.lastrowid
    except sqlite3.Error as e:
        raise DBError(f"Failed to append chapter: {str(e)}") from e

def get_chapter(conn: Connection, 
                chapter_id: int | None = None, 
                novel_id: int | None = None, 
                chapter_number: int | None = None) -> Optional[dict]:
    try:
        with conn:
            cursor = conn.cursor()
            if chapter_id is not None:
                cursor.execute("SELECT * FROM chapters WHERE id = ?", (chapter_id,))
            elif novel_id is not None and chapter_number is not None:
                cursor.execute("SELECT * FROM chapters WHERE novel_id = ? AND chapter_number = ?",(novel_id, chapter_number))
            else:
                return None
            row = cursor.fetchone()
            return _row_to_dict(row) if row else None
    except sqlite3.Error as e:
        raise DBError(f"Failed to get chapter: {str(e)}") from e

def get_chapters_by_novel(conn: Connection, novel_id: int) -> list[dict]:
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chapters WHERE novel_id = ?", (novel_id,))
        rows = cursor.fetchall()
        return [_row_to_dict(row) for row in rows]

def update_chapter(conn: Connection, 
                   chapter_id: int | None = None, 
                   chapter_number: int | None = None, 
                   title: str | None = None) -> bool:
    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT novel_id, chapter_number FROM chapters WHERE id = ?",
                (chapter_id,)
            )
            row = cursor.fetchone()
            if not row:
                return False

            novel_id, old_number = row

            if chapter_number is not None and chapter_number != old_number:
                new_number = chapter_number

                cursor.execute("""
                    UPDATE chapters
                    SET chapter_number = -1
                    WHERE id = ?
                """, (chapter_id,))

                if new_number > old_number:
                    _shift_down(cursor, novel_id, old_number, new_number)

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

            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to update chapter: {str(e)}") from e

def save_chapter_content(conn: Connection, 
                           chapter_id: int, 
                           content: str,
                           base_dir: str|None = None) -> str:
    try:
        with conn:
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

            return file_path, content_hash #TODO: content_hash not yet used
    except sqlite3.Error as e:
        raise DBError(f"Failed to save chapter content: {str(e)}") from e

def load_chapter_content(conn: Connection, chapter_id: int) -> Optional[str]:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT raw_file_path FROM chapters WHERE id = ?", (chapter_id,))
            row = cursor.fetchone()
            if not row or not row["raw_file_path"]:
                return None

            with open(row["raw_file_path"], "r", encoding="utf-8") as f:
                return f.read()
    except sqlite3.Error as e:
        raise DBError(f"Failed to load chapter content: {str(e)}") from e

def delete_chapter(conn: Connection, chapter_id: int) -> bool:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to delete chapter: {str(e)}") from e
