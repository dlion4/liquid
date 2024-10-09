

from __future__ import annotations


import typing
from allauth.account.utils import perform_login
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import login
from .models import User
from django.shortcuts import redirect
if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin
    from django.http import HttpRequest
    from amiribd.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self,request,sociallogin,data) -> User:
        user = super().populate_user(request, sociallogin, data)
        # Check if user with this email already exists
        if User.objects.filter(email=user.email).exists():
            # User already exists, handle authentication and redirect
            existing_user = User.objects.get(email=user.email)
            
            # Log the user in
            login(request, existing_user, backend='allauth.account.auth_backends.AuthenticationBackend')
            
            # Redirect to home page
            return redirect('home')  # Make sure 'home' is the name of your home URL pattern
        
        # If user doesn't exist, continue with the default flow (populate and return)
        return user
    def save_user(self, request, sociallogin, form=None):
        """
        If the user exists, skip the signup flow and log them in.
        """
        user = sociallogin.user

        # Check if the user already exists
        if User.objects.filter(email=user.email).exists():
            existing_user = User.objects.get(email=user.email)
            
            # Log the user in and return redirect
            perform_login(request, existing_user, email_verification=settings.ACCOUNT_EMAIL_VERIFICATION)
            
            # Redirect after login
            return redirect('home')

        # Proceed with the normal flow for new users
        return super().save_user(request, sociallogin, form)
