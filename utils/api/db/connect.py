import os
from typing import cast

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from config.settings.base import env
from litestar import Litestar
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): ...


DB_URI = "postgresql+asyncpg://postgres:1234@pg.db:5432/amiribd"


def get_db_connection(app: Litestar) -> AsyncEngine:
    """Returns the db engine.

    If it doesn't exist, creates it and saves it in on the application state object
    """
    if not getattr(app.state, "engine", None):
        app.state.engine = create_async_engine(DB_URI)
    return cast("AsyncEngine", app.state.engine)


async def close_db_connection(app: Litestar) -> None:
    """Closes the db connection stored in the application State object."""
    if getattr(app.state, "engine", None):
        await cast("AsyncEngine", app.state.engine).dispose()



async def init_db(app: Litestar) -> None:
    async with app.state.db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)