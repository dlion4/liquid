# import uuid

# from fastapi import FastAPI
# from sqlalchemy.ext.asyncio import async_sessionmaker

# from notes.crud import NoteCrud
# from notes.db import engine
# from notes.models import Note
# from notes.schemas import NoteModel

# app = FastAPI(
#     title="Note Taking Api",
#     description="An endpoint for notes api services for read and write",
#     docs_url="/",
# )


# session = async_sessionmaker(
#     bind=engine,
#     expire_on_commit=False
# )
# db = NoteCrud()


# @app.get("/notes", response_model=list[NoteModel])
# async def notes():
#     return await db.get_all_notes(session)


# @app.post("/notes")
# async def notes():  # noqa: F811
#     note = Note(
#         id=uuid.uuid4(),
#         title="This is a test note",
#         content="This is a test content ",
#     )
#     return await db.create_note(session, note)

# @app.get("/notes/{note_id}")
# async def note(note_id):
#     """
#     This Python async function retrieves a note from a database using the provided note_id.
#     :param note_id: The `note_id` parameter is the unique identifier or key that is used to retrieve a
#     specific note from the database. It is passed to the `note` function to fetch the corresponding note
#     information from the database
#     :return: The `note` object is being returned.
#     """
#     return await db.retrieve_note(session, note_id)

# @app.put("/notes/{note_id}")
# def update(note_id):
#     pass


# @app.delete("/notes/{note_id}")
# async def delete(note_id):
#     """
#     This Python function defines a route for deleting a note with a specific
#     ID using the FastAPI
#     framework.
#     :param note_id: The `note_id` parameter in the route `/notes/{note_id}` represents
#     the unique
#     identifier of the note that is being targeted for deletion. When a DELETE request is
#     made to this
#     endpoint with a specific `note_id`, it should trigger the deletion of the
#     corresponding note in the
#     system
#     """

import os
import django
import resend
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
settings.configure()
django.setup()
from config.settings.base import BASE_DIR

template_name = BASE_DIR / "amiribd" / "templates" / "account" / "mails" / "login.html"
html_message = render_to_string(template_name, {"killk": "link"})
plain_message = strip_tags(html_message)
params: resend.Emails.SendParams = {
    "from": "email@earnkraft.com",
    "to": ["liontechblue@gmail.com"],
    "subject": "hello world",
    "html": plain_message,
}

email = resend.Emails.send(params)
print(email)
