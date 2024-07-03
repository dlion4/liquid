from .models import Article, Template, TemplateCategory, YtSummarizer
from rest_framework import serializers
from amiribd.users.serializers import ProfileSerializer

class TemplateCategorySerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = TemplateCategory
        fields = "__all__"

    def get_posts(self, obj):
        # Serialize the articles related to this category's templates
        articles = obj.get_article_posts()
        return ArticleSerializer(articles, many=True).data

    def get_posts(self, obj):
        return obj.get_article_posts()
    



class TemplateSerializer(serializers.ModelSerializer):
    category = TemplateCategorySerializer()
    class Meta:
        model = Template
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    template = TemplateSerializer()
    # SerializerMethodField for custom boolean fields
    popular = serializers.SerializerMethodField()
    trending = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()


    class Meta:
        model = Article
        fields = "__all__"


    def get_popular(self, obj):
        return bool(obj.is_popular())
    
    def get_trending(self, obj):
        return bool(obj.is_trending())
    
    def get_image_url(self, obj):
        if obj.cover:
            return obj.cover.url
        return None


class YtSummarizerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = YtSummarizer
        fields = "__all__"

