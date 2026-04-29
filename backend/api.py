from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from grader.grader import *
from database.novel_db import create_novel
from database.chapter_db import get_chapter, save_chapter_content, load_chapter_content, create_chapter
from database.db import get_connection
from sqlite3 import Connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (fine for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

# TODO: Remoove this temp helper gunction once the other APT are added
def get_or_create_default_chapter(conn: Connection) -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM novels LIMIT 1")
    row = cursor.fetchone()

    if row:
        novel_id = row["id"]
    else:
        novel_id = create_novel(conn, "Default Novel")

    chapter = get_chapter(conn, novel_id=novel_id, chapter_number=1)

    if chapter:
        return chapter["id"]

    return create_chapter(conn, novel_id, 1, "Default Chapter")


@app.post("/grade")
def grade(req: TextRequest):
    conn = get_connection()

    chapter_id = get_or_create_default_chapter(conn)

    save_chapter_content(
        conn,
        chapter_id,
        req.text,
    )

    content = load_chapter_content(conn, chapter_id)

    doc = Document(content, get_nlp_model())
    annotated = grader.grade_text(doc)

    conn.close()

    return {"annotatedText": annotated}