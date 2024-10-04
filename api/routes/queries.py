from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import post
from sqlalchemy import select

from api.models import Post

if TYPE_CHECKING:

    from sqlalchemy.ext.asyncio import AsyncSession

@post("/")
async def add_post(data: Post, db_session: AsyncSession) -> list[Post]:
    async with db_session.begin():
        db_session.add(data)
    return (await db_session.execute(select(Post))).scalars().all()
