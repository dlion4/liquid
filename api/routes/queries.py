from __future__ import annotations
from sqlalchemy import select
from api.models import Post, Profile
from typing import TYPE_CHECKING
from litestar import post
if TYPE_CHECKING:

    from sqlalchemy.ext.asyncio import AsyncSession

@post("/")
async def add_post(data: Post, db_session: AsyncSession) -> list[Post]:
    async with db_session.begin():
        db_session.add(data)
    return (await db_session.execute(select(Post))).scalars().all()
