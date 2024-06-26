from litestar import Router, Controller, get, Litestar, Request
from pydantic import BaseModel
from amiribd.users.models import Profile
from amiribd.posts.models import Post
from typing import Optional, List
from django.http import JsonResponse
from datetime import datetime
from .serializers import PostSerializer, ProfileSerializer
from django.db.models import QuerySet
from asgiref.sync import sync_to_async
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class ProfileModel(BaseModel):
    first_name:str

class PostModel(BaseModel):
    id: int
    title: str
    slug:str
    content:Optional[str] = ''
    author: ProfileModel  # Use a string to refer to Profile
    date_posted: Optional[datetime]|None = None

    class Config:
        from_attributes = True  # This replaces orm_mode in Pydantic v2
        arbitrary_types_allowed = True  # Ignore unknown types

# Synchronous function to fetch posts
def get_posts_sync():
    return list(Post.objects.select_related('author').all().values(
        'id', 'title', 'slug','content', 'author__first_name', 'date_posted'
    ))

# Asynchronous view function to list posts
@get('/posts')
async def list_posts() -> list[PostModel]:
    try:
        # Retrieve and serialize posts using Django ORM in a synchronous context
        posts = await sync_to_async(get_posts_sync)()
        print("Retrieved posts:", posts)

        # Convert ORM data to Pydantic models
        data = [
            PostModel(
                id=post['id'],
                title=post['title'],
                slug=post['slug'],
                content=post['content'],
                author=ProfileModel(
                    first_name=post['author__first_name']
                ),
                date_posted=post['date_posted']
            )
            for post in posts
        ]
        print("Parsed data:", data)


        return data
    
    except Exception as exc:
        logger.error("Error in list_posts: %s", exc, exc_info=True)
        return {"detail": "Internal server error", "trace": str(exc)}


article_route_handler = Router(path="/apis/v1/articles", route_handlers=[list_posts])

