import json
import logging
import secrets
import string
import threading
import time
from urllib.parse import parse_qs

import requests
from django.conf import settings
from django.contrib.auth.models import User as UserObject
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models
from django.http import HttpRequest
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import base36_to_int
from django.utils.http import int_to_base36
from django.utils.http import urlsafe_base64_encode
from django.utils.timezone import timedelta

from .tasks import send_background_email

logger = logging.Logger(__file__)


class ConcatField(models.Func):
    arg_joiner = " || "
    function = None
    output_field = models.TextField()
    template = "%(expressions)s"


class BackgroundEmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        send_background_email(self.email)


class ExpiringTokenGenerator(PasswordResetTokenGenerator):
    """
        A token generator that creates expiring tokens for password reset.
        Explanation:
        Generates a token for password reset with an expiry time. The token includes
        the user's primary key and a timestamp indicating when the token was generated.
        timestamp and is validated based on the expiry time.

        Args:
        - self
        - user: The user for whom the token is generated.

        Returns:
        - str: The generated token.

        Raises:
        - None

        Example usage:
            >> token = expiring_token_generator.make_token(user)
            >> is_valid = expiring_token_generator.check_token(user, token)
    """

    # Expiry set to 5 minutes | will change later based on the requirements
    TOKEN_EXPIRY_TIMEOUT:int = 300 
    def make_token(self, user):
        timestamp = int(time.time())
        return f"{super().make_token(user)}-{int_to_base36(timestamp)}"

    def check_token(self, user, token):
        try:
            token, timestamp = token.rsplit("-", 1)
            timestamp = base36_to_int(timestamp)
        except (ValueError, TypeError):
            return False
        # Check token age
        if time.time() - timestamp > self.TOKEN_EXPIRY_TIMEOUT:  # The time duration for whcih the token remains valid
            return False
        return super().check_token(user, token)

expiring_token_generator = ExpiringTokenGenerator()


class BuildMagicLink:

    def _build_link_from_path(
        self, request:HttpRequest, path:str, kwds:dict | None=None,
        )->str:

        return request.build_absolute_uri(reverse(path, kwargs=kwds))

    def  build_url_from_path(
        self, request:HttpRequest, path:str, kwds:dict | None=None,
    ):
        """
        Builds a URL from a given path.

        Explanation:
        This function constructs a URL using the provided path, args, and kwargs.

        Args:
        - request: An HttpRequest object.
        - path: A string representing the path for the URL.
        - args: Additional positional arguments. (optional)
        - kwargs: Additional keyword arguments. (optional)

        Returns:
        The constructed URL.
        """
        return self._build_link_from_path(
            request, path, kwds,
        )

    def build_login_link_from_user(self, request:HttpRequest, user:UserObject):
        """
        Builds a login link for a given user.

        Args:
            request (HttpRequest): The HTTP request object.
            user (UserObject): The user object for which the login link is being built.

        Returns:
            str: The absolute URL of the login link.

        This method generates a login link for a given user by encoding the user's primary key
        and generating a token using the default token generator. It then constructs the login
        link by concatenating the user's encoded primary key, the generated token, and the
        "/users/login/" URL path. The resulting URL is obtained by calling the
        `build_absolute_uri` method on the request object.

        Example:
            If the user's primary key is 123 and the generated token is "abc", the login link
            will be "http://example.com/users/login/MTIzNA/abc/".
        """

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = expiring_token_generator.make_token(user)
        return self._build_link_from_path(
            request,"users:login_with_link",
            {"uid": uid,"token": token},
        )

    def send_login_email(
        self, user:UserObject,email_template:str= "accounts/mails/login.html", context:dict={}):  # noqa: B006, E501
        link = self.build_login_link_from_user(self.request, user)
        thread = threading.Thread(
            target=send_background_email,
            args=(
                user,
               email_template,
                {
                    "user": user,
                    "email":user.email,
                    "link": link,
                    "subject": "Login Request",
                    "extra": {k:v for k,v in context.items() if v is not None},
                },
            ),
        )
        thread.start()

    def send_signup_email(
        self, email,email_template:str="accounts/mails/signup.html", context:dict={},  # noqa: B006
        )->None:
        link=self._build_link_from_path(request=self.request, path="users:signup")
        thread = threading.Thread(target=send_background_email, args=(
            None, email_template,
            {
                "email": email,
                "link": link,
                "subject": "Earnkraft Registration",
                "from_email": "no-reply@earnkraft.com",
                "extra": {k:v for k,v in context.items() if v is not None},
            },
            None,
        ))
        thread.start()

    def send_welcome_email(
        self, email,email_template:str="accounts/mails/welcome/index.html", context:dict={},  # noqa: B006, E501
    )->None:
        """This is the welcome email sent wen a new user just register can be both for
        the
        Referred and the un referred users
        """
        thread = threading.Thread(target=send_background_email, args=(
            None, 
            email_template,
            {
                "email": email,
                "subject": "Welcome to Earnkraft Investment",
                "from_email": "no-reply@earnkraft.com",
                "policies":self.request.build_absolute_uri(reverse("policies")),
                "extra": {k:v for k,v in context.items() if v is not None},
            },
            None,
        ))
        thread.start()
        # Wait for the thread to complete
    def validate_email_address(self, email_address, *args, **kwargs) -> bool:
        """Validates an email address."""
        api_key = settings.ZERO_BOUNCE_EMAIL_VALIDATION_PROJECT_TOKEN
        headers = {"X-Mail-API-KEY": "Hello there guys this is a header test from the zerobunce api endpoitn"}
        endpoint = "https://zerobounce.pythonanywhere.com/api/v1/services/mails/validate"
        # try:
        #     response = requests.post(endpoint, data={"email": email_address}, headers=headers)
        #     response.raise_for_status()  # Raises an error for 4xx/5xx responses
        #     print(response.json())  # Log the response for debugging
        #     return response.status_code == 200
        # except requests.exceptions.HTTPError as http_err:
        #     logger.error(f"HTTP error occurred: {http_err} - Response content: {response.content if response else 'No response'}")
        #     if response and response.status_code == 403:
        #         try:
        #             error_response = response.json()  # Try to decode JSON response
        #             logger.error(f"Error detail: {error_response}")
        #         except ValueError:
        #             logger.error("Error response is not JSON")
        #     print(response.json())
        #     return False
        # except Exception as e:
        #     logger.error(f"Other error occurred: {e}")
        #     return False
        return True



    def validate_referral_code(self, code:str)->bool:
        """
        Validates a referral code.

        Args:
            code (str): The referral code to be validated.

        Returns:
            bool: True if the code is valid and not older than 7 days, False otherwise.

        Raises:
            ValueError: If the code does not have the expected format.

        This function splits the code into its components using the '-' delimiter.
        It checks if the prefix has the expected length. It then converts the timestamp
        to an integer and calculates the age of the code. Finally, it returns True if
        the code is valid and not older than 7 days, and False otherwise.

        Example:
            >>> validate_referral_code('cd-123-mk4567890123456789012345678901234567890123456789012345-1641343377')
            True
    """
        prefix_len:int = 2
        try:
            prefix, user_pk, random_str, timestamp = code.rsplit("-", 3)
            if len(prefix) != prefix_len:
                return False
            timestamp = int(timestamp)
        except ValueError:
            return False
        code_age = timezone.now() - timezone.datetime.fromtimestamp(
            timestamp, tz=timezone.utc)
        return not code_age > timedelta(days=7)

def generate_referral_code(user_pk):
    """
    Generates a referral code based on the provided user primary key.

    Parameters:
        user_pk (int): The primary key of the user.

    Returns:
        str: The generated referral code.

    Example:
        >>> generate_referral_code(123)
        'cd-123-mk4567890123456789012345678901234567890123456789012345-1641343377'
    """
    random_letters = "".join(secrets.choice(string.ascii_lowercase) for _ in range(2))
    random_str = "".join(
        secrets.choice(string.ascii_lowercase + string.digits) for _ in range(45))
    timestamp = int(time.time())
    return f"{random_letters}-{user_pk}-{random_str}-{timestamp}"


class PostCleanFormPostViewMixin:
    def ajax_filter_formatted_data(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid Post form data"})
        parsed_data = parse_qs(data)
        if "csrfmiddlewaretoken" in parsed_data:
            del parsed_data["csrfmiddlewaretoken"]
        return  {key: values[0] for key, values in parsed_data.items()}
    def fetch_filter_formatted_data(self,request):
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid Post form data"})


class EventEmitterView:
    def emit_authentication_event(self, user):
        if user is None:
            user_data = {"id": "", "email": ""}
        else:
            user_data = {"id": user.pk, "email": user.email}
        try:
            response = requests.post(
                "https://earnkraft-webhook.onrender.com/api/webhook",
                json=user_data,timeout=5,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.exception(f"HTTPError: {e} - Response: {response.text}")  # noqa: G004, TRY401
