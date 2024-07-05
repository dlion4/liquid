from src import User
from asgiref.sync import sync_to_async
from .schemas import UserCreateSchema
from src.posts.models import ProfileModel
from src.posts.schemas import Profile
from src import ProfileSerializer

class UserService:
    def get_user_by_email(self, email: str):
        # Use sync_to_async properly
        queryset =  User.objects.filter(email=email)
        # Now work with the queryset asynchronously
        if queryset.exists():
            return queryset.first()  # Return the first user found
        else:
            return None  # Return None if no user found
    
    def user_exists(self,email=None):
        user =  self.get_user_by_email(email=email)
        return True if user is not None else False
    
    def create_user(self, user_data:UserCreateSchema):
        user_data_dict = dict(user_data)  # Using dict() to convert Pydantic model to dict

        # Using sync_to_async to call synchronous Django ORM operations asynchronously
        new_user =   User.objects.create_user(**user_data_dict)

        return new_user

    def profile_service_object(self,email:str)->ProfileModel:
        profile = Profile.objects.get(user=self.get_user_by_email(email))
        return ProfileSerializer(profile).data

