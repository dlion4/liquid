from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from sqlalchemy.orm import DeclarativeBase

from .env import SQLALCHEMY_DB_URL


class Base(DeclarativeBase): ...



config = SQLAlchemyAsyncConfig(connection_string=SQLALCHEMY_DB_URL)
plugin = SQLAlchemyPlugin(config=config)




