from .models import Note
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy import String
from uuid import UUID

class NoteCrud:

    async def get_by_id(self, session:async_sessionmaker[AsyncSession], id:UUID):
        async with session() as sess:
            statement = select(Note).filter(Note.id == id)
            result = await sess.execute(statement)
            return result.scalars().one()
        

    async def get_all_notes(self, session:async_sessionmaker[AsyncSession]):
        async with session() as sess:
            statement = select(Note).order_by(Note.id)
            result = await sess.execute(statement)
            return result.scalars()
        
    async def create_note(self, session:async_sessionmaker[AsyncSession], note:Note):
        async with session() as sess:
            sess.add(note)
            await sess.commit()
            statement =  select(Note)
            result = await sess.execute(statement)
            return result.scalars().all() 

    async def retrieve_note(self, session:async_sessionmaker[AsyncSession], id:UUID):
        async with session() as sess:
            return await self.get_by_id(sess, id)
        
    async def delete_note(self, session:async_sessionmaker[AsyncSession], id:UUID):
        async with session() as sess:
            note = await self.get_by_id(sess, id)
            sess.delete(note)
            await sess.commit()


    async def update_note(self, session:async_sessionmaker[AsyncSession],id:str, data:Note):
        async with session() as sess:
            note = await self.get_by_id(sess, id)
            note.title = data['title']
            note.content = data['content']

            await sess.commit()

            return note

        
