import sqlite3
import pytest

from database.novel_db import *

def test_create_novel(conn):
    novel_id = create_novel(conn, "ABC")

    row = conn.execute(
        "SELECT * FROM novels WHERE id = ?",
        (novel_id,)
    ).fetchone()

    assert row["title"] == "ABC"

def test_duplicate_title(conn):
    create_novel(conn, "ABC")

    with pytest.raises(sqlite3.IntegrityError):
        create_novel(conn, "ABC")

def test_get_novel(conn):
    novel_id = create_novel(conn, "ABC")

    novel = get_novel(conn, novel_id)

    assert novel["title"] == "ABC"

def test_get_novels(conn):
    create_novel(conn, "A")
    create_novel(conn, "B")
    create_novel(conn, "C")

    novels = get_novels(conn)

    assert len(novels) == 3

def test_update_novel(conn):
    novel_id = create_novel(conn, "Old")

    result = update_novel(conn, novel_id, "New")

    updated = get_novel(conn, novel_id)

    assert result is True
    assert updated["title"] == "New"

def test_delete_novel(conn):
    novel_id = create_novel(conn, "ABC")

    result = delete_novel(conn, novel_id)

    row = get_novel(conn, novel_id)

    assert result is True
    assert row is None