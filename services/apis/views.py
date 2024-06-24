

# from services.apis.articles.views import article_route_handler
from typing import Dict
from services.apis.articles.views import PostModel, article_route_handler
from amiribd.posts.models import Post

from litestar import Litestar, get, Request

from litestar import Litestar

# app = Litestar(route_handlers=[article_route_handler])


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