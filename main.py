from fastapi import FastAPI
from notes.crud import NoteCrud
from sqlalchemy.ext.asyncio import async_sessionmaker
from notes.db import engine
from notes.schemas import NoteModel
from typing import List
from notes.models import Note
import uuid

app = FastAPI(
    title="Note Taking Api",
    description="An endpoint for notes api services for read and write",
    docs_url="/",
)


session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
db = NoteCrud()



@app.get("/notes", response_model=List[NoteModel])
async def notes():
    notes = await db.get_all_notes(session)
    return notes


@app.post("/notes")
async def notes():
    note = Note(
        id=uuid.uuid4(),
        title="This is a test note",
        content="This is a test content "
    )
    note = await db.create_note(session, note)
    return note

@app.get("/notes/{note_id}")
async def note(note_id):
    note = await db.retrieve_note(session, note_id)
    return note

@app.put("/notes/{note_id}")
def update(note_id):
    pass

@app.delete("/notes/{note_id}")
async def delete(note_id):
    pass
