import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import django

django.setup()

from amiribd.articles.models import Article, TemplateCategory
from amiribd.articles.serializers import ArticleSerializer, TemplateCategorySerializer

