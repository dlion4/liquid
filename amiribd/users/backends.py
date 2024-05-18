from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from amiribd.tokens.models import AuthToken
from django.contrib.auth import get_user_model
import logging


User = get_user_model()
logger = logging.getLogger(__name__)
from django.contrib.auth.backends import ModelBackend


class TokenAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, code=None):
        logger.debug(f"Authenticating code: {code}")
        try:
            user = User.objects.get(email=username)
            logger.debug(f"User {user} authenticated successfully")
            return user
        except User.DoesNotExist:
            logger.error("AuthToken does not exist or is not active")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
