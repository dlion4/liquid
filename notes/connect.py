from db import Base, engine
import asyncio
async def create_database():
    async with engine.begin() as conn:
        from models import Note
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

asyncio.run(create_database())