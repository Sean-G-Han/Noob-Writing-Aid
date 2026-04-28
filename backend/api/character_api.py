from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection

from database.db import get_connection
from models import CharacterCreate, CharacterResponse, CharacterUpdate
from database.character_db import (
    create_character,
    get_character,
    get_characters_by_chapter,
    update_character,
    delete_character,
)

router = APIRouter(prefix="/characters")

@router.post("/", response_model=CharacterResponse)
def create(data: CharacterCreate, db: Connection = Depends(get_connection)):
    character_id = create_character(db, 
        common_name=data.common_name, 
        adjectives=data.adjectives, 
        description=data.description, 
        pronouns=data.pronouns, 
        alternative_names=data.alternative_names, 
    chapters=data.chapters)
    return get_character(db, character_id)

@router.get("/{character_id}", response_model=CharacterResponse)
def read_one(character_id: int, db: Connection = Depends(get_connection)):
    character = get_character(db, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.get("/chapter/{chapter_id}", response_model=list[CharacterResponse])
def read_by_chapter(chapter_id: int, db: Connection = Depends(get_connection)):
    return get_characters_by_chapter(db, chapter_id)

@router.put("/{character_id}", response_model=CharacterResponse)
def update(character_id: int, data: CharacterUpdate, db: Connection = Depends(get_connection)):
    success = update_character(db, character_id, 
        common_name=data.common_name, 
        adjectives=data.adjectives, 
        description=data.description, 
        pronouns=data.pronouns, 
        alternative_names=data.alternative_names, 
        chapters=data.chapters)
    if not success:
        raise HTTPException(status_code=404, detail="Character not found")
    return get_character(db, character_id)

@router.delete("/{character_id}")
def delete(character_id: int, db: Connection = Depends(get_connection)):
    success = delete_character(db, character_id)
    if not success:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"ok": True}