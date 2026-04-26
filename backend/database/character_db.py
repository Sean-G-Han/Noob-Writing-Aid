from typing import Optional
from sqlite3 import Connection

def _character_row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "common_name": row["common_name"],
        "description": row["description"],
    }

def create_character(conn: Connection, 
                     common_name: str,
                     adjectives: list[str] | None = None,
                     description: str = "",
                     pronouns: list[str] | None = None,
                     alternative_names: list[str] | None = None,
                     chapters: list[int] | None = None) -> int:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO characters (common_name, description)
        VALUES (?, ?)
    """, (common_name, description))

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
            _link_character_to_chapter(conn, cursor.lastrowid, chapter_id)

    conn.commit()

    return cursor.lastrowid

# REVIEW: Should get return Character object directly?
def get_character_by_id(conn: Connection, character_id: int) -> Optional[dict]:
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

def get_characters_by_chapter(conn: Connection, chapter_id: int) -> list[dict]:
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

def update_character(conn: Connection, character_id: int, 
                     common_name: str,
                     adjectives: list[str] | None = None,
                     description: str = "",
                     pronouns: list[str] | None = None,
                     alternative_names: list[str] | None = None,
                     chapters: list[int] | None = None) -> bool:
    
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE characters
        SET common_name = ?, description = ?
        WHERE id = ?
    """, (common_name, description, character_id))

    # TODO: Very inefficient to remove all and re-add. Should only update the differences. 
    # But this is simpler to implement for now.
    if adjectives is not None:
        _remove_all_character_adjectives(conn, character_id)
        for adjective in adjectives:
            _add_character_adjective(conn, character_id, adjective)
    if pronouns is not None:
        _remove_all_character_pronouns(conn, character_id)
        for pronoun in pronouns:
            _add_character_pronoun(conn, character_id, pronoun)
    if alternative_names is not None:
        _remove_all_character_alt_names(conn, character_id)
        for alternative_name in alternative_names:
            _add_character_alt_name(conn, character_id, alternative_name)
    if chapters is not None:
        _unlink_all_character_from_chapter(conn, character_id)
        for chapter_id in chapters:
            _link_character_to_chapter(conn, character_id, chapter_id)

    conn.commit()
    
    return cursor.rowcount > 0

def delete_character(conn: Connection, character_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM characters
        WHERE id = ?
    """, (character_id,))
    conn.commit()
    return cursor.rowcount > 0

def _link_character_to_chapter(conn: Connection, character_id: int, chapter_id: int) -> int:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chapter_to_character (character_id, chapter_id)
        VALUES (?, ?)
    """, (character_id, chapter_id))
    return cursor.lastrowid

# def _unlink_character_from_chapter(conn: Connection, character_id: int, chapter_id: int) -> bool:
#     cursor = conn.cursor()
#     cursor.execute("""
#         DELETE FROM chapter_to_character
#         WHERE character_id = ? AND chapter_id = ?
#     """, (character_id, chapter_id))
#     return cursor.rowcount > 0

def _unlink_all_character_from_chapter(conn: Connection, character_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM chapter_to_character
        WHERE character_id = ?
    """, (character_id,))
    return cursor.rowcount > 0

def _add_character_adjective(conn: Connection, character_id: int, adjective: str) -> int:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO character_adjectives (character_id, adjective)
        VALUES (?, ?)
    """, (character_id, adjective))
    return cursor.lastrowid

def _get_character_adjectives(conn: Connection, character_id: int) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT adjective FROM character_adjectives
        WHERE character_id = ?
    """, (character_id,))
    return [row["adjective"] for row in cursor.fetchall()]

# def _remove_character_adjective(conn: Connection, character_id: int, adjective: str) -> bool:
#     cursor = conn.cursor()
#     cursor.execute("""
#         DELETE FROM character_adjectives
#         WHERE character_id = ? AND adjective = ?
#     """, (character_id, adjective))
#     return cursor.rowcount > 0

def _remove_all_character_adjectives(conn: Connection, character_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM character_adjectives
        WHERE character_id = ?
    """, (character_id,))
    return cursor.rowcount > 0

def _add_character_pronoun(conn: Connection, character_id: int, pronoun: str) -> int:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO character_pronouns (character_id, pronoun)
        VALUES (?, ?)
    """, (character_id, pronoun))
    return cursor.lastrowid

def _get_character_pronouns(conn: Connection, character_id: int) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pronoun FROM character_pronouns
        WHERE character_id = ?
    """, (character_id,))
    return [row["pronoun"] for row in cursor.fetchall()]

# def _remove_character_pronoun(conn: Connection, character_id: int, pronoun: str) -> bool:
#     cursor = conn.cursor()
#     cursor.execute("""
#         DELETE FROM character_pronouns
#         WHERE character_id = ? AND pronoun = ?
#     """, (character_id, pronoun))
#     return cursor.rowcount > 0

def _remove_all_character_pronouns(conn: Connection, character_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM character_pronouns
        WHERE character_id = ?
    """, (character_id,))
    return cursor.rowcount > 0

def _add_character_alt_name(conn: Connection, character_id: int, alternative_name: str) -> int:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO character_alternative_names (character_id, alternative_name)
        VALUES (?, ?)
    """, (character_id, alternative_name))
    return cursor.lastrowid

def _get_character_alt_names(conn: Connection, character_id: int) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT alternative_name FROM character_alternative_names
        WHERE character_id = ?
    """, (character_id,))
    return [row["alternative_name"] for row in cursor.fetchall()]

# def _remove_character_alt_name(conn: Connection, character_id: int, alternative_name: str) -> bool:
#     cursor = conn.cursor()
#     cursor.execute("""
#         DELETE FROM character_alternative_names
#         WHERE character_id = ? AND alternative_name = ?
#     """, (character_id, alternative_name))
#     return cursor.rowcount > 0

def _remove_all_character_alt_names(conn: Connection, character_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM character_alternative_names
        WHERE character_id = ?
    """, (character_id,))
    return cursor.rowcount > 0