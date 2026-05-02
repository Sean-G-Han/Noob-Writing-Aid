import sqlite3
import os
from sqlite3 import Connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nwa.db")

# Have to be a regular return
def get_connection() -> Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: Connection, schema_path="database/schema.sql"):
    cursor = conn.cursor()

    with open(schema_path, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()


def reset_db(conn: Connection, schema_path="database/schema.sql"):
    cursor = conn.cursor()

    cursor.executescript("""
        DROP TABLE IF EXISTS character_alternative_names;
        DROP TABLE IF EXISTS character_pronouns;
        DROP TABLE IF EXISTS character_adjectives;
        DROP TABLE IF EXISTS characters;
        DROP TABLE IF EXISTS chapter_to_character;
        DROP TABLE IF EXISTS chapters;
        DROP TABLE IF EXISTS novels;
    """)

    with open(schema_path, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()


if __name__ == "__main__":
    conn = get_connection()
    try:
        reset_db(conn)
        init_db(conn)
        print("Database initialized successfully.")
    finally:
        conn.close()