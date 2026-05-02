from typing import Optional
from sqlite3 import Connection
import sqlite3
from database.exceptions import DBError

def _character_row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "common_name": row["common_name"],
        "description": row["description"],
    }

def create_character(conn: Connection, 
                     novel_id: int,
                     common_name: str,
                     adjectives: list[str] | None = None,
                     description: str = "",
                     pronouns: list[str] | None = None,
                     alternative_names: list[str] | None = None,
                     chapters: list[int] | None = None) -> int:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO characters (novel_id, common_name, description)
                VALUES (?, ?, ?)
            """, (novel_id, common_name, description))

            if adjectives:
                for adjective in adjectives:
                    _add_character_adjective(conn, cursor.lastrowid, adjective)
            if pronouns:
                for pronoun in pronouns:
                    _add_character_pronoun(conn, cursor.lastrowid, pronoun)
            if alternative_names:
                for alternative_name in alternative_names:
                    _add_character_alt_name(conn, cursor.lastrowid, alternative_name)
            if chapters:
                for chapter_id in chapters:
                    link_character_to_chapter(conn, cursor.lastrowid, chapter_id)

            conn.commit()

            return cursor.lastrowid
    except sqlite3.Error as e:
        raise DBError(f"Failed to create character: {str(e)}") from e

# REVIEW: Should get return Character object directly?
def get_character(conn: Connection, character_id: int) -> Optional[dict]:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM characters
                WHERE id = ?
            """, (character_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            
            data = _character_row_to_dict(row)
            data["adjectives"] = _get_character_adjectives(conn, character_id)
            data["pronouns"] = _get_character_pronouns(conn, character_id)
            data["alternative_names"] = _get_character_alt_names(conn, character_id)

            return data
    except sqlite3.Error as e:
        raise DBError(f"Failed to get character: {str(e)}") from e

def get_characters_by_chapter(conn: Connection, chapter_id: int) -> list[dict]:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.* FROM characters c
                JOIN chapter_to_character cc ON c.id = cc.character_id
                WHERE cc.chapter_id = ?
            """, (chapter_id,))
            rows = cursor.fetchall()

            characters = []
            for row in rows:
                data = _character_row_to_dict(row)
                data["adjectives"] = _get_character_adjectives(conn, data["id"])
                data["pronouns"] = _get_character_pronouns(conn, data["id"])
                data["alternative_names"] = _get_character_alt_names(conn, data["id"])
                characters.append(data)

            return characters
    except sqlite3.Error as e:
        raise DBError(f"Failed to get characters by chapter: {str(e)}") from e

def get_characters_by_novel(conn: Connection, novel_id: int) -> list[dict]:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM characters
                WHERE novel_id = ?
            """, (novel_id,))
            rows = cursor.fetchall()

            characters = []
            for row in rows:
                data = _character_row_to_dict(row)
                data["adjectives"] = _get_character_adjectives(conn, data["id"])
                data["pronouns"] = _get_character_pronouns(conn, data["id"])
                data["alternative_names"] = _get_character_alt_names(conn, data["id"])
                characters.append(data)

            return characters
    except sqlite3.Error as e:
        raise DBError(f"Failed to get characters by novel: {str(e)}") from e    

def update_character(conn: Connection, character_id: int, 
                     common_name: str,
                     adjectives: list[str] | None = None,
                     description: str = "",
                     pronouns: list[str] | None = None,
                     alternative_names: list[str] | None = None,
                     chapters: list[int] | None = None) -> bool:
    try:
        with conn:
            cursor = conn.cursor()

            updates = []
            params = []

            if common_name is not None:
                updates.append("common_name = ?")
                params.append(common_name)

            if description is not None:
                updates.append("description = ?")
                params.append(description)

            if updates:
                query = f"""
                    UPDATE characters
                    SET {", ".join(updates)}
                    WHERE id = ?
                """
                params.append(character_id)
                cursor.execute(query, params)

            if adjectives is not None:
                _remove_all_character_adjectives(conn, character_id)
                for adj in adjectives:
                    _add_character_adjective(conn, character_id, adj)

            if pronouns is not None:
                _remove_all_character_pronouns(conn, character_id)
                for pro in pronouns:
                    _add_character_pronoun(conn, character_id, pro)

            if alternative_names is not None:
                _remove_all_character_alt_names(conn, character_id)
                for name in alternative_names:
                    _add_character_alt_name(conn, character_id, name)

            if chapters is not None:
                _unlink_all_character_from_chapter(conn, character_id)
                for ch_id in chapters:
                    link_character_to_chapter(conn, character_id, ch_id)

            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to update character: {str(e)}") from e

def delete_character(conn: Connection, character_id: int) -> bool:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM chapter_to_character
                WHERE character_id = ?
            """, (character_id,))
            cursor.execute("""
                DELETE FROM characters
                WHERE id = ?
            """, (character_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to delete character: {str(e)}") from e

def link_character_to_chapter(conn: Connection, character_id: int, chapter_id: int) -> int:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chapter_to_character (character_id, chapter_id)
                VALUES (?, ?)
            """, (character_id, chapter_id))
            return cursor.lastrowid
    except sqlite3.Error as e:
        raise DBError(f"Failed to link character to chapter: {str(e)}") from e

def unlink_character_from_chapter(conn: Connection, character_id: int, chapter_id: int) -> bool:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM chapter_to_character
                WHERE character_id = ? AND chapter_id = ?
            """, (character_id, chapter_id))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to unlink character from chapter: {str(e)}") from e

def _unlink_all_character_from_chapter(conn: Connection, character_id: int) -> bool:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM chapter_to_character
                WHERE character_id = ?
            """, (character_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to unlink character from chapters: {str(e)}") from e

def _add_character_adjective(conn: Connection, character_id: int, adjective: str) -> int:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO character_adjectives (character_id, adjective)
                VALUES (?, ?)
            """, (character_id, adjective))
            return cursor.lastrowid
    except sqlite3.Error as e:
        raise DBError(f"Failed to add adjective: {str(e)}") from e

def _get_character_adjectives(conn: Connection, character_id: int) -> list[str]:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT adjective FROM character_adjectives
                WHERE character_id = ?
            """, (character_id,))
            return [row["adjective"] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise DBError(f"Failed to get adjectives: {str(e)}") from e

# def _remove_character_adjective(conn: Connection, character_id: int, adjective: str) -> bool:
#     with conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             DELETE FROM character_adjectives
#             WHERE character_id = ? AND adjective = ?
#         """, (character_id, adjective))
#         return cursor.rowcount > 0

def _remove_all_character_adjectives(conn: Connection, character_id: int) -> bool:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM character_adjectives
                WHERE character_id = ?
            """, (character_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to remove adjectives: {str(e)}") from e

def _add_character_pronoun(conn: Connection, character_id: int, pronoun: str) -> int:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO character_pronouns (character_id, pronoun)
                VALUES (?, ?)
            """, (character_id, pronoun))
            return cursor.lastrowid
    except sqlite3.Error as e:
        raise DBError(f"Failed to add pronoun: {str(e)}") from e

def _get_character_pronouns(conn: Connection, character_id: int) -> list[str]:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pronoun FROM character_pronouns
                WHERE character_id = ?
            """, (character_id,))
            return [row["pronoun"] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise DBError(f"Failed to get pronouns: {str(e)}") from e

# def _remove_character_pronoun(conn: Connection, character_id: int, pronoun: str) -> bool:
#     try:
#         with conn:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 DELETE FROM character_pronouns
#                 WHERE character_id = ? AND pronoun = ?
#             """, (character_id, pronoun))
#             return cursor.rowcount > 0
#     except sqlite3.Error as e:
#         raise DBError(f"Failed to remove pronoun: {str(e)}") from e

def _remove_all_character_pronouns(conn: Connection, character_id: int) -> bool:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM character_pronouns
                WHERE character_id = ?
            """, (character_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to remove pronouns: {str(e)}") from e

def _add_character_alt_name(conn: Connection, character_id: int, alternative_name: str) -> int:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO character_alternative_names (character_id, alternative_name)
                VALUES (?, ?)
            """, (character_id, alternative_name))
            return cursor.lastrowid
    except sqlite3.Error as e:
        raise DBError(f"Failed to add alternative name: {str(e)}") from e

def _get_character_alt_names(conn: Connection, character_id: int) -> list[str]:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT alternative_name FROM character_alternative_names
                WHERE character_id = ?
            """, (character_id,))
            return [row["alternative_name"] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise DBError(f"Failed to get alternative names: {str(e)}") from e

# def _remove_character_alt_name(conn: Connection, character_id: int, alternative_name: str) -> bool:
#     with conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             DELETE FROM character_alternative_names
#             WHERE character_id = ? AND alternative_name = ?
#         """, (character_id, alternative_name))
#         return cursor.rowcount > 0

def _remove_all_character_alt_names(conn: Connection, character_id: int) -> bool:
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM character_alternative_names
                WHERE character_id = ?
            """, (character_id,))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise DBError(f"Failed to remove alternative names: {str(e)}") from e