from typing import Any
from django.shortcuts import redirect
from django.urls import reverse

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class AuthenticationStateCheckMiddleware(MiddlewareMixin):
    """
    Middleware to check if the user is authenticated.
    Redirects to login page if the user is not authenticated.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        # List of paths to skip the authentication check
        exempt_paths = [
            reverse('users:login'),
            reverse('users:signup'),
            reverse('users:logout')
        ]

        # Add patterns that require additional parameters
        exempt_paths += [
            reverse(
                'users:login-redirect', 
                 kwargs={
                     'uid': 'uid_placeholder',
                     'token': 'token_placeholder'
                     }
                ).replace('uid_placeholder/', '').replace('token_placeholder/', ''),
            reverse(
                'users:referred-signup',
                kwargs={
                    'referral_code': 'referral_placeholder'
                    }
                ).replace('referral_placeholder/', '')
        ]

        # Check if the current path starts with any exempt path
        if any(request.path.startswith(path) for path in exempt_paths):
            return None

        # Check if the user is not authenticated
        if not request.user.is_authenticated:
            return redirect('users:login')

        return None

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)



