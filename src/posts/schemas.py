from ninja.orm import create_schema
from src import Article
from src import Profile
from src import Template
from src import TemplateCategory
from src import User
from src import YtSummarizer

UserSchema = create_schema(
    User,
    exclude=[
        "password",
        "last_login",
        "is_superuser",
        "is_staff",
        "groups",
        "user_permissions",
        "date_joined",
    ],
)
ProfileSchema = create_schema(
    Profile,
    exclude=[
        "job_applications",
        "plans",
        "adverts",
        "image",
        "accepted_job_applications",
    ],
)
ArticleSchema = create_schema(Article, exclude=[])
TemplateSchema = create_schema(Template, exclude=[])
TemplateCategorySchema = create_schema(TemplateCategory, exclude=[])
YtSummarizerSchema = create_schema(YtSummarizer, exclude=[])
