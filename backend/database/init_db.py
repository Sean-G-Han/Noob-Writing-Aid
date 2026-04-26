from sqlite3 import Connection
from .db import get_connection
from .cursor_singleton import CursorSingleton

def init_db(conn: Connection, schema_path="database/schema.sql"):
    cursor = CursorSingleton.get_instance(conn)

    with open(schema_path, "r") as f:
        cursor.executescript(f.read())

    conn.commit()

def reset_db(conn: Connection, schema_path="database/schema.sql"):
    cursor = CursorSingleton.get_instance(conn)

    cursor.executescript("""
        DROP TABLE IF EXISTS character_alternative_names;
        DROP TABLE IF EXISTS character_pronouns;
        DROP TABLE IF EXISTS character_adjectives;
        DROP TABLE IF EXISTS characters;
        DROP TABLE IF EXISTS chapter_to_character;
        DROP TABLE IF EXISTS chapters;
        DROP TABLE IF EXISTS novels;
    """)

    with open(schema_path, "r") as f:
        cursor.executescript(f.read())

    conn.commit()

if __name__ == "__main__":
    conn: Connection = get_connection()
    reset_db(conn)
    init_db(conn)
    print("Database initialized successfully.")