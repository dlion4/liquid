from typing import list

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from amiribd.articles.models import YtSummarizer
from amiribd.articles.serializers import YtSummarizerSerializer
from src.authentication.dependencies import AccessTokenBearer
from src.posts.models import YtSummarizerModel
from src.posts.services import PostService

from . import Article
from . import ArticleModel
from . import ArticleSerializer
from . import TemplateCategory
from . import TemplateCategoryModel
from . import TemplateCategorySerializer
from . import router

post_services = PostService()

access_token_bearer = AccessTokenBearer()


@router.get("/posts",response_model=list[ArticleModel],status_code=status.HTTP_200_OK)
def test_sync_to_async()->list[ArticleModel]:
    try:
        return ArticleSerializer(Article.objects.all(),many=True).data
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))  # noqa: B904

@router.get(
    "/podcasts", response_model=list[YtSummarizerModel], status_code=status.HTTP_200_OK)
def get_podcasts()->list[YtSummarizerModel]:
    try:
        podcasts = YtSummarizer.objects.select_related("profile").filter(is_verified=True)  # noqa: E501
        return YtSummarizerSerializer(podcasts, many=True).data
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))  # noqa: B904


@router.get("/podcasts/{podcast_id}")
def get_podcast(podcast_id:int)->YtSummarizerModel:
    try:
        podcast = YtSummarizer.objects.get(pk=podcast_id)
        return YtSummarizerSerializer(podcast).data
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))  # noqa: B904


@router.get("/categories", response_model=list[TemplateCategoryModel])
def get_post_categories()->list[TemplateCategoryModel]:
    try:
        return TemplateCategorySerializer(TemplateCategory.objects.all(), many=True).data
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))  # noqa: B904


@router.get("/posts/comments")
def retrieve_post_comment(
    user_details=Depends(access_token_bearer)):  # noqa: B008
    return {"message": "Something great is cooking"}


@router.get(
    "/posts/{slug}",
    response_description="Return a post that matches the given slug",
    response_model_by_alias=False, response_model=ArticleModel)
def get_post(slug:str):

    return post_services.get_post_by_slug(slug, Model=Article)
