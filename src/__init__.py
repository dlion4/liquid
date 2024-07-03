# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from datetime import datetime
# import django

# django.setup()
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from src.posts.views import router as posts_router

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)