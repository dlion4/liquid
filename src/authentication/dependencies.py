from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request
from fastapi.exceptions import HTTPException
from src.authentication.service import UserService
from src.utils import decode_token
from src.redis import token_in_blocklist
from fastapi import Depends

user_service_object = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
        # self.token_type = "access_token"
    async def __call__(self, request:Request)->HTTPAuthorizationCredentials|None:
        creds= await super().__call__(request)
        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(status_code=401,  detail={
                "error":"Invalid or expired token",
                "resolution":"Please get a new token"
            })

        if token_in_blocklist(token_data['jti']):
            print("helo ", token_in_blocklist(token_data['jti']))
            raise HTTPException(status_code=401, detail={
                "error":"This token is invalid or has been revoked",
                "resolution":"Please get a new token"
            })
        

        self.verify_token_data(token_data)

        return token_data
    
    def token_valid(self, token:str)->bool:
        token_data = decode_token(token)

        return True if token_data is not None else False
    
    def verify_token_data(self, token)->None:
        raise NotImplementedError("You'll need to implement this method")
    

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict)->None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=401, detail="Please provide an access token")

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict)->None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=401, detail="Please provide a refresh token")


def get_current_user(token_data:dict=Depends(AccessTokenBearer())):
    email =  token_data['user']['email']
    # user = user_service_object.get_user_by_email(email)
    profile = user_service_object.profile_service_object(email=email)
    return profile

