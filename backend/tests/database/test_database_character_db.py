import sqlite3
import pytest

from database.character_db import *
from database.novel_db import create_novel, delete_novel
from database.chapter_db import create_chapter
from context.character import Character

def test_create_character(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id=novel_id, chapter_number=1, title="Chapter 1")
    char1 = Character(
        common_name="ABC",
        adjectives={"A", "B"},
        description="ABCDEF",
        pronouns={"he", "him", "his"},
        alternative_names={"ABCD"}
    )
    character_id = create_character(conn,
                                    novel_id=novel_id,
                                    common_name="ABC",
                                    adjectives=["A", "B"], 
                                    description="ABCDEF", 
                                    pronouns=["he", "him", "his"], 
                                    alternative_names=["ABCD"],
                                    chapters=[chapter_id])

    char2 = Character.from_dict(get_character(conn, character_id))

    assert char1 == char2

def test_link_character_to_chapter(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id=novel_id, chapter_number=1, title="Chapter 1")
    
    characters_in_chapter = get_characters_by_chapter(conn, chapter_id)
    assert len(characters_in_chapter) == 0

    character_id = create_character(conn, novel_id=novel_id, common_name="ABC", chapters=[chapter_id])

    characters_in_chapter = get_characters_by_chapter(conn, chapter_id)
    assert len(characters_in_chapter) == 1
    assert characters_in_chapter[0]["id"] == character_id

    unlink_character_from_chapter(conn, chapter_id=chapter_id, character_id=character_id)

    characters_in_chapter = get_characters_by_chapter(conn, chapter_id)
    assert len(characters_in_chapter) == 0


def test_get_character_nonexistent(conn):
    char_data = get_character(conn, 99999)
    assert char_data is None

def test_cascade_delete(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id=novel_id, chapter_number=1, title="Chapter 1")
    character_id = create_character(conn, novel_id=novel_id, common_name="ABC", chapters=[chapter_id])

    delete_novel(conn, chapter_id)

    char_data = get_character(conn, character_id)
    assert char_data is not None

def test_update_character(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id1 = create_chapter(conn, novel_id=novel_id, chapter_number=1, title="Chapter 1")
    chapter_id2 = create_chapter(conn, novel_id=novel_id, chapter_number=2, title="Chapter 2")
    character_id = create_character(conn,
                                    novel_id=novel_id,
                                    common_name="ABC",
                                    adjectives=["A", "B"], 
                                    description="ABCDEF", 
                                    pronouns=["he", "him", "his"], 
                                    alternative_names=["ABCD"],
                                    chapters=[chapter_id1])
    
    char1 = Character.from_dict(get_character(conn, character_id))

    char2 = Character(
        common_name="XYZ",
        adjectives={"C", "D"},
        description="XYZ123",
        pronouns={"she", "her", "hers"},
        alternative_names={"Z"}
    )

    assert char1 != char2

    update_character(conn, character_id, 
                     common_name="XYZ", 
                     adjectives={"C", "D"},
                     description="XYZ123",
                     pronouns={"she", "her", "hers"},
                     alternative_names={"Z"},
                     chapters={chapter_id2})

    char1 = Character.from_dict(get_character(conn, character_id))

    assert char1 == char2

    char_from_chapter2 = get_characters_by_chapter(conn, chapter_id2)
    assert len(char_from_chapter2) == 1

def test_delete_character(conn):
    novel_id = create_novel(conn, "ABC")
    chapter_id = create_chapter(conn, novel_id=novel_id, chapter_number=1, title="Chapter 1")
    character_id = create_character(conn, novel_id=novel_id, common_name="ABC", chapters=[chapter_id])

    char_data = get_character(conn, character_id)
    assert char_data is not None

    delete_character(conn, character_id)

    char_data = get_character(conn, character_id)
    assert char_data is None


