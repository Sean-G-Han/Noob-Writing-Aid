import sqlite3
import pytest

from database.novel_db import create_novel, delete_novel
from database.chapter_db import *
from database.cursor_singleton import CursorSingleton

def test_create_chapter(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Chapter 1")

    row = conn.execute(
        "SELECT * FROM chapters WHERE id = ?",
        (chapter_id,)
    ).fetchone()

    assert row["novel_id"] == novel_id
    assert row["chapter_number"] == 1
    assert row["title"] == "Chapter 1"

def test_cascade_delete(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Chapter 1")

    delete_novel(conn, novel_id)

    row = conn.execute(
        "SELECT * FROM chapters WHERE id = ?",
        (chapter_id,)
    ).fetchone()

    assert row is None

def test_duplicate_chapter_title(conn):
    novel_id = create_novel(conn, "ABC")
    create_chapter(conn, novel_id, 1, "Chapter 1")

    with pytest.raises(sqlite3.IntegrityError):
        create_chapter(conn, novel_id, 1, "Chapter 1")

def test_get_chapter(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Chapter 1")

    chapter = get_chapter(conn, chapter_id)

    assert chapter["novel_id"] == novel_id
    assert chapter["chapter_number"] == 1
    assert chapter["title"] == "Chapter 1"

def test_get_chapter_by_novel_and_number(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Chapter 1")
    chapter_id_2 = create_chapter(conn, novel_id, 2, "Chapter 2")

    chapter = get_chapter(conn, novel_id=novel_id, chapter_number=1)
    chapter_2 = get_chapter(conn, novel_id=novel_id, chapter_number=2)

    assert chapter["id"] == chapter_id
    assert chapter_2["id"] == chapter_id_2

def test_get_nonexistent_chapter(conn):
    chapter = get_chapter(conn, 9999)
    assert chapter is None

def test_get_chapter_invalid_args(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Chapter 1")
    chapter = get_chapter(conn)
    assert chapter is None

    chapter = get_chapter(conn, novel_id=1)
    assert chapter is None

    chapter = get_chapter(conn, chapter_number=1)
    assert chapter is None

    chapter = get_chapter(conn, chapter_id=chapter_id, chapter_number=1)

def test_get_chapters_by_novel(conn):
    novel_id = create_novel(conn, "ABC")
    create_chapter(conn, novel_id, 1, "Chapter 1")
    create_chapter(conn, novel_id, 2, "Chapter 2")

    chapters = get_chapters_by_novel(conn, novel_id)

    assert len(chapters) == 2

def test_update_chapter(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Chapter 1")

    result = update_chapter(conn, chapter_id, "Updated Chapter")

    updated = get_chapter(conn, chapter_id)

    assert result is True
    assert updated["title"] == "Updated Chapter"

#YH Note: tmp_path is a pytest fixture that provides a temporary directory for testing file operations.
def test_update_chapter_content(conn, tmp_path):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id=novel_id, chapter_number=1, title="Test")

    content = "Hello world"

    file_path = update_chapter_content(
        conn,
        chapter_id,
        content,
        base_dir=tmp_path
    )

    assert os.path.exists(file_path)

    cursor = CursorSingleton.get_instance(conn)
    cursor.execute("SELECT raw_file_path FROM chapters WHERE id = ?", (chapter_id,))
    row = cursor.fetchone()
    assert row["raw_file_path"] == file_path

def test_get_chapter_content(conn, tmp_path):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Test")

    content = "Some content"
    update_chapter_content(conn, chapter_id, content, base_dir=tmp_path)

    result = get_chapter_content(conn, chapter_id)

    assert result == content

def test_get_chapter_content_no_file(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Test")
    result = get_chapter_content(conn, chapter_id)
    assert result is None

def test_get_chapter_content_file_missing(conn, tmp_path):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Test")
    content = "Hello"
    file_path = update_chapter_content(conn, chapter_id, content, base_dir=tmp_path)
    os.remove(file_path)
    pytest.raises(FileNotFoundError, get_chapter_content, conn, chapter_id)

def test_delete_chapter(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id, 1, "Chapter 1")

    result = delete_chapter(conn, chapter_id)

    row = get_chapter(conn, chapter_id)

    assert result is True
    assert row is None