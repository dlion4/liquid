
from pydantic import  Field, Secret
from datetime import date
from typing import Optional, List
from src.posts.schemas import (
UserSchema,
ProfileSchema,
ArticleSchema,
TemplateSchema,
TemplateCategorySchema,
YtSummarizerSchema,
)
from typing_extensions import Annotated



class SecretEmail(Secret[str]):
    def _display(self) -> str:
        return "some*****@webestica.com"
    
class SecretPhoneNumber(Secret[str]):
    def _display(self)->str:
        return "(***) (****) (**) (***)"
    
SecretDate = Secret[date]

class ArticleModel(ArticleSchema):
    profile:Optional['ProfileModel']=None
    template:Optional['TemplateModel']|None = None


class TemplateCategoryModel(TemplateCategorySchema):
    posts:List[ArticleModel]=[]


class TemplateModel(TemplateSchema):
    category: TemplateCategoryModel
    is_premium:bool


class UserModel(UserSchema):
    email:SecretEmail

class ProfileModel(ProfileSchema):
    user: UserModel
    image_url:Annotated[str, Field(default_factory=str)]
    phone_number: SecretPhoneNumber
    date_of_birth: SecretDate
    refered_by: Optional["ProfileModel"] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.image_url and self.image:
            self.image_url = self.image.url
        self.refered_by = self


class YtSummarizerModel(YtSummarizerSchema):
    profile:ProfileModel|None = None

