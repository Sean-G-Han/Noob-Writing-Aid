import sqlite3
import pytest
from database.init_db import init_db

#YH Notes: this gives a connection to in-mem SQLite DB
@pytest.fixture(scope="session") # YH Notes: Basically like a wrapper for the test functions
def conn(): #called whenever conn is used as an argument in a test function
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    
    conn.execute("PRAGMA foreign_keys = ON")
    init_db(conn, schema_path="database/schema.sql")

    yield conn # YH Notes: returns and waits for test function to finish
    conn.close()

@pytest.fixture(autouse=True) # YH Notes: runs before each test function without needing to be called
def reset_db(conn):
    yield # makes staments run AFTER
    conn.executescript(
        "DELETE FROM chapter_to_character;\n"
        "DELETE FROM character_adjectives;\n"
        "DELETE FROM character_pronouns;\n"
        "DELETE FROM character_alternative_names;\n"
        "DELETE FROM chapters;\n"
        "DELETE FROM characters;\n"
        "DELETE FROM novels;\n"
        "DELETE FROM sqlite_sequence;" # YH Notes: resets autoincrement IDs back to 1
    )
    conn.commit()