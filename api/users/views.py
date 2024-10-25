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
            login_tokens = {
                "accessToken": access_token,
                "refreshToken": refresh_token,
            }
            return Response(login_tokens, status=status.HTTP_200_OK)
        return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)


class UserTokenValidation(APIView, JWTAuthentication, BuildMagicLink):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        user, token = self.authenticate(request)
        if user:
            self.send_login_email(user, "account/dashboard/v1/mails/login.html")
            return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
        return  Response(
            {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
