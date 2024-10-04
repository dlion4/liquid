from litestar import Controller
from litestar import Router
from litestar import get
from litestar import post
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Post


class PostController(Controller):
    path = "/posts"

    @get()
    async def get_posts(self, db_session:AsyncSession)->list[Post]:
        result = await db_session.execute(select(Post))
        return result.scalars().all()
    @post()
    async def create_post(self, data:Post, db_session:AsyncSession)->dict:
        async with db_session.begin():
            db_session.add(data)
        await db_session.commit()
        return {"data":"data"}



posts_route = Router(path="/",route_handlers=[PostController])
