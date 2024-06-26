from litestar import Litestar
from api.utils.db import init_db
from api.settings import plugin
from api.controlers import posts_route



app = Litestar(route_handlers=[posts_route], on_startup=[init_db], plugins=[plugin])