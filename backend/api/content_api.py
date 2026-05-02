from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection

from database.db import get_connection
from .models import ChapterSave, ChapterSaveResponse, ChapterLoadResponse
from database.chapter_db import save_chapter_content, load_chapter_content
from database.character_db import get_characters_by_chapter
from grader.grader import Grader
from context.character import CharacterRegistry, Character
from components.components import Document
from util import get_nlp_model

router = APIRouter(prefix="/content")

@router.post("/save/{chapter_id}", response_model=ChapterSaveResponse)
def save_chapter(chapter_id: int, data: ChapterSave, db: Connection = Depends(get_connection)):
    
    try:
        file_path, content_hash = save_chapter_content(
            db,
            chapter_id,
            data.content,
            data.base_dir if data.base_dir else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "file_path": file_path,
        "hash": content_hash
    }

@router.get("/load/{chapter_id}", response_model=ChapterLoadResponse)
def load_chapter(chapter_id: int, db: Connection = Depends(get_connection)):
    
    content = load_chapter_content(db, chapter_id)

    if content is None:
        raise HTTPException(status_code=404, detail="Chapter content not found")

    return {
        "content": content
    }

@router.post("/grade/{chapter_id}")
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