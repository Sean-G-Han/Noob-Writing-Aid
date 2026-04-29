from api import novel_api, character_api, grade_api, chapter_api, content_api
from fastapi import FastAPI

app = FastAPI()

app.include_router(novel_api.router)
app.include_router(character_api.router)
app.include_router(grade_api.router)
app.include_router(chapter_api.router)
app.include_router(content_api.router)
