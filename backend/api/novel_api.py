from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection

from database.db import get_connection
from models import NovelCreate, NovelUpdate, NovelResponse, BooleanResponse
from database.novel_db import (
    create_novel,
    get_novel,
    get_novels,
    update_novel,
    delete_novel,
)

router = APIRouter(prefix="/novels")

#YH Note: Response models forces dictionary output to have the specified fields, so we can return a dict with only those fields.
#YH Note 2: Depends is like spring's @Autowired, it injects the dependency 
@router.post("/", response_model=NovelResponse)
def create(data: NovelCreate, db: Connection = Depends(get_connection)):
    novel_id = create_novel(db, data.title)
    return get_novel(db, novel_id)

@router.get("/", response_model=list[NovelResponse])
def read_all(db: Connection = Depends(get_connection)):
    return get_novels(db)

@router.get("/{novel_id}", response_model=NovelResponse)
def read_one(novel_id: int, db: Connection = Depends(get_connection)):
    novel = get_novel(db, novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    return novel

@router.put("/{novel_id}", response_model=NovelResponse)
def update(novel_id: int, data: NovelUpdate, db: Connection = Depends(get_connection)):
    success = update_novel(db, novel_id, data.title)
    if not success:
        raise HTTPException(status_code=404, detail="Novel not found")
    return {"id": novel_id, "title": data.title}

@router.delete("/{novel_id}", response_model=BooleanResponse)
def delete(novel_id: int, db: Connection = Depends(get_connection)):
    success = delete_novel(db, novel_id)
    if not success:
        raise HTTPException(status_code=404, detail="Novel not found")
    return {"ok": True}