
from pydantic import Field

from ninja import Schema


class UserCreateSchema(Schema):
    name:str=Field(max_length=20)
    email:str=Field(max_length=40)
    username: str | None = Field(max_length=100)
    password:str=Field(min_length=6)

class UserLoginSchema(Schema):
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)

class UserProfileUpdateSchema(Schema):
    first_name:str
    last_name:str
    username:str
    bio:str
