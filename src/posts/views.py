from amiribd.articles.models import YtSummarizer
from amiribd.articles.serializers import YtSummarizerSerializer
from src.posts.models import YtSummarizerModel
from . import (
    router, 
    ArticleModel,
    TemplateCategoryModel,
    TemplateModel,
    UserModel,
    ProfileModel,
    ArticleSerializer, 
    TemplateCategorySerializer,
    Article, 
    TemplateCategory
)
from typing import List, Dict, Optional
from fastapi import  HTTPException, status


@router.get("/posts",response_model=List[ArticleModel],status_code=status.HTTP_200_OK)
def test_sync_to_async()->List[ArticleModel]:
    try:
        data = ArticleSerializer(Article.objects.all(),many=True).data
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/podcasts", response_model=List[YtSummarizerModel], status_code=status.HTTP_200_OK)
def get_podcasts()->List[YtSummarizerModel]:
    try:
        podcasts = YtSummarizer.objects.select_related('profile').filter(is_verified=True)
        data = YtSummarizerSerializer(podcasts, many=True).data
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/podcasts/{podcast_id}")
def get_podcast(podcast_id:int)->YtSummarizerModel:
    try:
        podcast = YtSummarizer.objects.get(pk=podcast_id)
        data = YtSummarizerSerializer(podcast).data
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories", response_model=List[TemplateCategoryModel])
def get_post_categories()->List[TemplateCategoryModel]:
    try:
        return TemplateCategorySerializer(TemplateCategory.objects.all(), many=True).data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))