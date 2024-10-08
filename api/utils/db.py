
from litestar import Litestar

from api.settings import Base


async def init_db(app: Litestar) -> None:
    async with app.state.db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
