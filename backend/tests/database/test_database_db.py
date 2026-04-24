import sqlite3

from database.db import get_connection

def test_get_connection():
    conn = get_connection()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()