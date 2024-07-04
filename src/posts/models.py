
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from fastapi import UploadFile


class ArticleModel(BaseModel):
    id:int
    profile:Optional['ProfileModel']=None
    template:Optional['TemplateModel']|None = None
    title:str
    slug: str 
    summary:str=''
    content:str=''
    created_at:datetime 
    updated_at:datetime 
    release_date:datetime 


    views:int
    archived:bool
    featured :bool
    reads:int

    image_url:str|None=None

    popular:bool
    trending:bool

    editorsPick:bool
    sponsored:bool
    
    recommeded:bool


class TemplateCategoryModel(BaseModel):
    id: int
    title:str
    description:str
    timestamp: datetime
    icon:str
    posts:List[ArticleModel]=[]
    color:str


class TemplateModel(BaseModel):
    id:int
    category: TemplateCategoryModel
    is_premium:bool


class UserModel(BaseModel):
    id:int
    email: str
    username: str
    verified: bool


class ProfileModel(BaseModel):
    id: int
    user:UserModel
    first_name: str
    last_name: str
    image_url:Optional[str]=None
    full_name:str
    kyc_completed: bool
    kyc_validated: bool
    kyc_completed_at: datetime
    is_address_set: bool
    is_document_set: bool
    phone_number: str
    date_of_birth: datetime
    initials: str
    referral_code: str
    referred_by: Optional[int] = None
    name_initials: Optional[str] = 'ES'



class YtSummarizerModel(BaseModel):
    id:int
    profile:ProfileModel|None = None
    title:str|None="This is un untitled podcast."
    video_url:str|None = None
    timestamp:datetime
    summary:str
    transcript_file:str|None = None
    audio_url:str|None = None
    is_processed:bool = False
    duration:int = None
    size:int = None
    video_transcript:str = None
    is_verified:bool = True
