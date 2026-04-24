from sqlite3 import Connection
from .db import get_connection

def init_db(conn: Connection, schema_path="database/schema.sql"):
    cursor = conn.cursor()

    with open(schema_path, "r") as f:
        cursor.executescript(f.read())

    conn.commit()

if __name__ == "__main__":
    init_db(get_connection())
    print("Database initialized successfully.")