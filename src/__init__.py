import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import django

django.setup()

from amiribd.articles.models import Article, TemplateCategory, Template, YtSummarizer
from amiribd.articles.serializers import ArticleSerializer, TemplateCategorySerializer
from amiribd.users.models import User, Profile
from amiribd.users.serializers import ProfileSerializer
from .config import config
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from src.posts.views import router as posts_router
from src.authentication import router as auth_router

load_dotenv(dotenv_path="./.env")
version=os.environ.get('API_VERSION', "1.0")


app = FastAPI(
    title="EarnKraft Post API",
    description="An API for EarnKraft's services and functionalities",
    docs_url="/",
    version=version,
    port="",
)


app.include_router(posts_router, prefix="/api/{version}")
app.include_router(auth_router, prefix="/api/{version}", tags=['Authentication Endpoints'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)