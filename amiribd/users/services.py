import datetime
import uuid

import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.request import Request

from config.setup import load_keys

from .models import User

# Key configurations for JWT
RSA_PRIVATE_KEY = load_keys()[0]
RSA_PUBLIC_KEY = load_keys()[1]
JWT_EXPIRATION_DELTA = 3600  # 1 hour for access token
JWT_REFRESH_EXPIRATION_DELTA = 86400 * 7  # 7 days for refresh token


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        auth = request.headers.get("Authorization", None)
        if not auth:
            return None
        try:
            token_type, token = auth.split()
            if token_type.lower() != "bearer":
                msg = "Authorization header must start with Bearer"
                raise exceptions.AuthenticationFailed(
                    msg,
                )

            if token_type.lower() == "bearer":
                return self.authenticate_access_token(token)
        except ValueError as e:
            msg = "Invalid authorization header format"
            raise exceptions.AuthenticationFailed(msg) from e

    def authenticate_access_token(self, token):
        try:
            payload = jwt.decode(
                token,
                RSA_PUBLIC_KEY,
                algorithms=["RS256"],
                options={"verify_aud": True},  # Enable audience verification
                audience=settings.JWT_AUDIENCE,  # Check audience
                issuer=settings.JWT_ISSUER,  # Check issuer
            )
            user = User.objects.get(id=payload["user_id"])
            return (user, token)  # noqa: TRY300

        except jwt.ExpiredSignatureError as e:
            msg = "Access token has expired"
            raise exceptions.AuthenticationFailed(msg) from e

        except jwt.InvalidTokenError as e:
            msg = "Invalid access token"
            raise exceptions.AuthenticationFailed(msg) from e

    @staticmethod
    def generate_access_token(user):
        payload = {
            "user_id": str(user.id),
            "exp": datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(seconds=JWT_EXPIRATION_DELTA),
            "iat": datetime.datetime.now(datetime.UTC),
            "jti": str(uuid.uuid4()),  # JWT ID for uniqueness
            "iss": settings.JWT_ISSUER,
            "aud": settings.JWT_AUDIENCE,
        }
        return jwt.encode(payload, RSA_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def generate_refresh_token(user):
        payload = {
            "user_id": str(user.id),
            "exp": datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(seconds=JWT_REFRESH_EXPIRATION_DELTA),
            "refresh": True,
            "iat": datetime.datetime.now(datetime.UTC),  # Issued at
            "jti": str(uuid.uuid4()),  # JWT ID for uniqueness
            "iss": settings.JWT_ISSUER,
            "aud": settings.JWT_AUDIENCE,
        }
        return jwt.encode(payload, RSA_PRIVATE_KEY, algorithm="RS256")
