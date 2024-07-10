from src import User, Profile, TemplateCategory, Article, Template, YtSummarizer
from ninja.orm import create_schema

UserSchema = create_schema(User,exclude=['password', 'last_login', 'is_superuser', 'is_staff', 'groups', 'user_permissions', "date_joined", ])
ProfileSchema = create_schema(Profile, exclude=["job_applications", "plans", "adverts","image", ])
ArticleSchema = create_schema(Article, exclude=[])
TemplateSchema = create_schema(Template, exclude=[])
TemplateCategorySchema = create_schema(TemplateCategory, exclude=[])
YtSummarizerSchema = create_schema(YtSummarizer, exclude=[])