from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    url='postgresql+asyncpg://postgres:1234@localhost:5432/notes',
    echo=True
)


class Base(DeclarativeBase): ...