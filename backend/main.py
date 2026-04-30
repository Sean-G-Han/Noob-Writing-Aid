from api import novel_api, character_api, grade_api, chapter_api, content_api
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database.exceptions import DBError

app = FastAPI()

@app.exception_handler(DBError)
async def unique_constraint_handler(request: Request, exc: DBError):
    return JSONResponse(
        status_code=409,
        content={"message": "Duplicate entry", "detail": str(exc)},
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (fine for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(novel_api.router)
app.include_router(character_api.router)
app.include_router(grade_api.router)
app.include_router(chapter_api.router)
app.include_router(content_api.router)
