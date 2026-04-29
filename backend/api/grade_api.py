from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection

from database.db import get_connection
from database.chapter_db import load_chapter_content
from database.character_db import get_characters_by_chapter
from grader.grader import Grader
from context.character import CharacterRegistry, Character
from components.components import Document
from util import get_nlp_model

router = APIRouter(prefix="/grade")

@router.post("/{chapter_id}")
def grade_chapter(chapter_id: int, db: Connection = Depends(get_connection)):

    content = load_chapter_content(db, chapter_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Chapter content not found")

    char_registry = CharacterRegistry()
    characters = get_characters_by_chapter(db, chapter_id)
    for c in characters:
        char_registry.register(Character.from_dict(c))

    doc = Document(content, get_nlp_model(), char_registry)

    grader = Grader()
    annotated = grader.grade_text(doc)

    return {"annotatedText": annotated}