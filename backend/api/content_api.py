from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection

from database.db import get_connection
from models import ChapterSave, ChapterSaveResponse, ChapterLoadResponse
from database.chapter_db import save_chapter_content, load_chapter_content
router = APIRouter(prefix="/content")

@router.post("/save", response_model=ChapterSaveResponse)
def save_chapter(data: ChapterSave, db: Connection = Depends(get_connection)):
    
    try:
        file_path, content_hash = save_chapter_content(
            db,
            data.chapter_id,
            data.content,
            data.base_dir if data.base_dir else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "file_path": file_path,
        "hash": content_hash
    }

@router.get("/{chapter_id}/load", response_model=ChapterLoadResponse)
def load_chapter(chapter_id: int, db: Connection = Depends(get_connection)):
    
    content = load_chapter_content(db, chapter_id)

    if content is None:
        raise HTTPException(status_code=404, detail="Chapter content not found")

    return {
        "content": content
    }
