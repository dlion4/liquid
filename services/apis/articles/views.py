from litestar import Router, Controller, get, Litestar, Request
from pydantic import BaseModel
from amiribd.users.models import Profile
from amiribd.posts.models import Post
from typing import Optional, List
from django.http import JsonResponse
from datetime import datetime

class ProfileModel(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class PostModel(BaseModel):
    id: int
    title: str
    slug:str
    content:str
    author: 'Profile'  # Use a string to refer to Profile
    date_posted: Optional[datetime]|None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True  # Ignore unknown types

@get("/posts")
async def list_posts(request:Request)->List[PostModel]:
    posts = Post.objects.all()
    print(posts)
    data = [PostModel(post) for post in posts]
    return JsonResponse(data, safe=False)

article_route_handler = Router(path="/apis/v1/articles", route_handlers=[list_posts])

