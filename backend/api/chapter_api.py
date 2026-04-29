from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection

from database.db import get_connection
from .models import ChapterCreate, ChapterUpdate, ChapterResponse
from database.chapter_db import (
    create_chapter,
    get_chapter,
    get_chapters_by_novel,
    update_chapter,
    delete_chapter,
)

router = APIRouter(prefix="/chapters")

@router.post("/", response_model=ChapterResponse)
def create(data: ChapterCreate, db: Connection = Depends(get_connection)):
    chapter_id = create_chapter(db, data.novel_id, data.chapter_number, data.title)
    return get_chapter(db, chapter_id=chapter_id)

@router.get("/{chapter_id}", response_model=ChapterResponse)
def read_one(chapter_id: int, db: Connection = Depends(get_connection)):
    chapter = get_chapter(db, chapter_id=chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@router.get("/novel/{novel_id}", response_model=list[ChapterResponse])
def read_by_novel(novel_id: int, db: Connection = Depends(get_connection)):
    return get_chapters_by_novel(db, novel_id)

@router.put("/{chapter_id}", response_model=ChapterResponse)
def update(chapter_id: int, data: ChapterUpdate, db: Connection = Depends(get_connection)):
    success = update_chapter(db, chapter_id, data.chapter_number, data.title)
    if not success:
        raise HTTPException(status_code=404, detail="Chapter not found")
    chapter = get_chapter(db, chapter_id=chapter_id)
    return chapter

@router.delete("/{chapter_id}")
def delete(chapter_id: int, db: Connection = Depends(get_connection)):
    success = delete_chapter(db, chapter_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {"ok": True}
