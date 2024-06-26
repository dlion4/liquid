

# from services.apis.articles.views import article_route_handler
from typing import Dict
from services.apis.articles.views import PostModel, article_route_handler
from amiribd.posts.models import Post

from litestar import Litestar, get, Request

from litestar import Litestar

import logging

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a custom handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a custom formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)


@get("/apis/v1/omera")
async def hello_world(request:Request) -> Dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    # posts = Post.objects.all()
    print("Hello people")
    print("posts")
    # print([PostModel(**post) for post in posts])
    return {"hello": "world"}

@get("/apis/v1/tesla")
async def tesla(request:Request) -> Dict[str, str]:
    # print(Post.objects.all())
    return {"hello": "tesla"}

app = Litestar(route_handlers=[hello_world, tesla, article_route_handler])