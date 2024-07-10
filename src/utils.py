from src import config
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError
from datetime import timedelta, datetime,date
import uuid
import jwt
import logging

ACCESS_TOKEN_EXPIRY=3600



def create_access_token(user_data:dict, expiry:timedelta=None, refresh:bool=False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now()+(expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=config.JWT_AUTH_SECRET,
        algorithm=config.JWT_AUTH_ALGORITHM
    )

    return token


def pad_base64_token(token: str) -> str:
    padding_needed = 4 - (len(token) % 4)
    if padding_needed:
        token += "=" * padding_needed
    return token

def decode_token(token: str) -> dict:
    try:
        padded_token = pad_base64_token(token)
        token_data = jwt.decode(
            jwt=padded_token,
            key=config.JWT_AUTH_SECRET,
            algorithms=[config.JWT_AUTH_ALGORITHM]
        )
        return token_data
    except (DecodeError, ExpiredSignatureError, InvalidTokenError) as e:
        logging.exception(e)
        return None