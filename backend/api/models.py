from pydantic import BaseModel

class BooleanResponse(BaseModel):
    ok: bool

class GraderRequest(BaseModel):
    chapter_id: int

class GraderResponse(BaseModel):
    annotated_text: str

class NovelCreate(BaseModel):
    title: str

class NovelUpdate(BaseModel):
    title: str

class NovelResponse(BaseModel):
    id: int
    title: str

class ChapterCreate(BaseModel):
    novel_id: int
    chapter_number: int
    title: str

class ChapterAppend(BaseModel):
    novel_id: int
    title: str

class ChapterUpdate(BaseModel):
    chapter_number: int | None
    title: str | None

class ChapterResponse(BaseModel):
    id: int
    novel_id: int
    chapter_number: int
    title: str
    raw_file_path: str | None
    annotated_file_path: str | None
    hash: str | None

class ChapterSave(BaseModel):
    content: str
    base_dir: str | None = None

class ChapterSaveResponse(BaseModel):
    file_path: str
    hash: str

class ChapterLoadResponse(BaseModel):
    content: str

class CharacterCreate(BaseModel):
    novel_id: int
    common_name: str
    description: str = ""
    adjectives: list[str] | None = None
    pronouns: list[str] | None = None
    alternative_names: list[str] | None = None
    chapters: list[int] | None = None

class CharacterUpdate(BaseModel):
    common_name: str | None = None
    description: str | None = None
    adjectives: list[str] | None = None
    pronouns: list[str] | None = None
    alternative_names: list[str] | None = None
    chapters: list[int] | None = None

class CharacterLink(BaseModel):
    chapter_id: int
    character_id: int

class CharacterResponse(BaseModel):
    id: int
    common_name: str
    description: str
    adjectives: list[str]
    pronouns: list[str]
    alternative_names: list[str]