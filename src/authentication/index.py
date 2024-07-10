from src.authentication import router
from fastapi import  HTTPException, Depends, APIRouter, Security, status
from ninja.security import django_auth
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from typing_extensions import Annotated
from src.authentication.schemas import UserCreateSchema, UserLoginSchema, UserProfileUpdateSchema
from src.posts.models import UserModel
from .service import UserService
from src.utils import create_access_token, decode_token
from datetime import timedelta
from fastapi.responses import JSONResponse
from src.authentication.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user
from datetime import datetime
from src.redis import add_to_blocklist


router = APIRouter(prefix="/auth")

header_scheme = APIKeyHeader(name="earnkraft-x-key")

security = HTTPBearer()

user_service_object = UserService()

@router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
def create_user_account(user_data:UserCreateSchema)->UserModel:
    email = user_data.email

    user_exists =  user_service_object.user_exists(email)


    print(user_exists)

    if user_exists:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    user =  user_service_object.create_user(user_data)
    return user


@router.post("/login",status_code=status.HTTP_200_OK)
def login_user(user_login_data:UserLoginSchema):
    email = user_login_data.email
    password = user_login_data.password

    print(user_login_data)

    user = user_service_object.get_user_by_email(email)
    if user is not None:
        if user.check_password(password):
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.id)
                    }
                )
            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.id)
                },
                refresh=True,
                expiry=timedelta(days=30)  # 30 days expiry for refresh token
    
            )
            return JSONResponse(
                content={
                    "message":"Login successful",
                    "access_token":access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "id": str(user.id)
                    }
                }
            )
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user credentials")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user credentials")


@router.get("/refresh_token")
def retrieve_new_access_token(token_details:dict=Depends(RefreshTokenBearer())):

    expiry_timestamp = token_details['exp']
    print(expiry_timestamp)

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        return JSONResponse(content={
            "access_token": new_access_token
            })

    raise HTTPException(status_code=400, detail="Invalid or Expired token")


@router.get("/logout")
def logout_user(token_details:dict=Depends(AccessTokenBearer())):
    jti = token_details['jti']
    add_to_blocklist(jti)
    return JSONResponse(content={"message":"Logged out successfully"}, status_code=200)


@router.get("/dashboard")
def get_current_user_(profile=Depends(get_current_user)):
    return profile


@router.post("/profile/update")
def update_current_user(user_data:UserProfileUpdateSchema, token_data:dict=Depends(AccessTokenBearer())):
    email = token_data['user']['email']
    user = user_service_object.get_user_by_email(email)
    # Remove the username from the dictionary
    profile_data = user_data.model_dump()
    username = profile_data.pop("username", None)  # Removes 'username' key if it exists
    user.username = username
    user.save()
    # Print the remaining data (for debugging purposes)
    user.profile_user.first_name = profile_data['first_name']
    user.profile_user.last_name = profile_data['last_name']
    user.profile_user.save()
    # Update the user's profile (if needed)
    # profile = user  # Depending on your implementation, you might update the profile here
    # Return the remaining data without the username
    profile = user_service_object.profile_service_object(email)
    return profile



    