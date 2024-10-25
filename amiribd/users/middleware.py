from base64 import b64decode

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import Resolver404
from django.urls import resolve
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class AuthenticationStateCheckMiddleware(MiddlewareMixin):
    """
    Middleware to check if the user is authenticated.
    Redirects to login page if the user is not authenticated.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def get_unprotected_route(self):
        return [
            reverse("home"),
            reverse("about"),
            # reverse("investment"),  # noqa: ERA001
            reverse("learn"),
            reverse("contact"),
            reverse("help"),
            reverse("guide"),
            reverse("customers"),
            reverse("career"),
            reverse("policies"),
            # reverse("view_policy", kwargs={"pk": 1}),  # noqa: ERA001
        ]

    def process_request(self, request):
        # List of paths to skip the authentication check
        exempt_paths = [
            reverse("users:login"),
            reverse("users:signup"),
            reverse("users:logout"),
        ]

        exempt_paths += self.get_unprotected_route()

        # Add patterns that require additional parameters
        exempt_paths += [
            reverse(
                "users:login_with_link",
                 kwargs={"uid": "uid_placeholder","token": "token_placeholder"},
                ).replace("uid_placeholder/", "").replace("token_placeholder/", ""),
            reverse(
                "users:referred-signup",
                kwargs={"referral_code": "referral_placeholder"},
                ).replace("referral_placeholder/", ""),
        ]

        # Check if the current path starts with any exempt path
        if any(request.path.startswith(path) for path in exempt_paths):
            return None

        # Check if the user is not authenticated
        if not request.user.is_authenticated:
            return redirect("users:login")

        return None

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)


class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Apply the middleware only to /silk/ URL
        if not request.path.startswith("/silk/"):
            return self.get_response(request)  # Allow access to non-/silk/ requests
        # Check if Authorization header is present
        if "HTTP_AUTHORIZATION" not in request.META:
            return self._request_authentication()

        # Extract and decode the Authorization header
        auth_type, credentials = request.META["HTTP_AUTHORIZATION"].split(" ", 1)
        if auth_type.lower() != "basic":
            return self._request_authentication()

        decoded_credentials = b64decode(credentials).decode("utf-8")
        username, password = decoded_credentials.split(":", 1)

        # Replace 'your_username' and 'your_password' with your actual credentials
        if username == "earnkraft_silk_username" and password == "earnkraft_silk_password":
            return self.get_response(request)  # Allow access if credentials match

        return self._request_authentication()

    def _request_authentication(self):
        # Return 401 Unauthorized response to prompt for credentials
        response = HttpResponse("Unauthorized", status=401)
        response["WWW-Authenticate"] = 'Basic realm="Silk Access"'
        return response

