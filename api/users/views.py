import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from amiribd.users.models import User
from amiribd.users.services import JWTAuthentication
from amiribd.users.utils import BuildMagicLink

from .serializers import LoginSerializer


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    token = JWTAuthentication()
    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.filter(email=data.get("email"))
        if user.exists():
            user = user.first()
            access_token = self.token.generate_access_token(user)
            refresh_token = self.token.generate_refresh_token(user)
            login_tokens = {"accessToken": access_token,"refreshToken": refresh_token}
            return Response(login_tokens, status=status.HTTP_200_OK)
        return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)


    def options(self, request):
        response = Response(status=status.HTTP_200_OK)
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "https://auth.earnkraft.com"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        print(response)
        return response


class UserTokenValidation(APIView, BuildMagicLink):
    permission_classes = [permissions.AllowAny]
    token = JWTAuthentication()

    def post(self, request, *args, **kwargs):
        user, _ = self.token.authenticate(request)
        if user:
            self.send_login_email(user, "account/dashboard/v1/mails/login.html")
            return Response({"message": "Token is valid", "success": True},status=status.HTTP_200_OK)  # noqa: E501
        return  Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)  # noqa: E501

    def options(self, request):
        response = Response(status=status.HTTP_200_OK)

        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "https://auth.earnkraft.com"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"

        return response


class UserValidateAccessToken(APIView):
    permission_classes = [permissions.AllowAny]
    token = JWTAuthentication()
    def post(self, request, *args, **kwargs):
        user, _ = self.token.authenticate(request)
        if user:
            return Response({"message": "Token is valid", "success": True},status=status.HTTP_200_OK)  # noqa: E501
        return  Response({"error": "Invalid token"},status=status.HTTP_401_UNAUTHORIZED)

    def options(self, request):
        response = Response(status=status.HTTP_200_OK)

        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "https://auth.earnkraft.com"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"

        return response


class ValidateAuthenticatedUserView(APIView):
    permission_classes = [permissions.AllowAny]
    token = JWTAuthentication()
    def post(self, request, *args, **kwargs):
        user, _ = self.token.authenticate(request)
        if user:
            return Response({"message": "Token is valid", "success": True},status=status.HTTP_200_OK)  # noqa: E501
        return Response({}, status.HTTP_400_BAD_REQUEST)

    def options(self, request):
        response = Response(status=status.HTTP_200_OK)

        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "https://auth.earnkraft.com"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"

        return response


class CheckAuthenticationStatusView(View):


    @method_decorator(csrf_exempt)
    def get(self, request, *args, **kwargs):
        user_email = request.GET.get("email_address")

        if not user_email:
            return JsonResponse({}, status=400)
        try:
            user = User.objects.get(email=user_email)
            return JsonResponse(
                {"user_email": user.email, "is_authenticated": user.is_authenticated},
                status=200,
            )
        except User.DoesNotExist:
            return JsonResponse({}, status=404)

    def options(self, request):
        response = Response(status=status.HTTP_200_OK)
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "https://auth.earnkraft.com"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"

        return response