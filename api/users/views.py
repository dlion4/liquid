from django.db import IntegrityError
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from amiribd.users.models import Profile
from amiribd.users.models import User
from amiribd.users.models import User as UserObject
from amiribd.users.services import JWTAuthentication
from amiribd.users.utils import BuildMagicLink
from amiribd.users.utils import generate_referral_code

from .serializers import LoginSerializer
from .serializers import UserRegistrationSerializer


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


class UserRegisterView(APIView, BuildMagicLink):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                self.send_welcome_email(email=user.email)
                return Response(
                    {"message": "User registered successfully."},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                return Response(
                    {"message": "A user with this email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReferralSignupView(APIView, BuildMagicLink):
    permission_classes = [permissions.AllowAny]

    def _validate_code(self, code: str) -> bool:
        return bool(code and self.validate_referral_code(code))

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        referral_code = kwargs.get("referral_code")

        if not self._validate_code(referral_code):
            return Response(
                {"message": "Invalid or expired referral code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            try:
                user = self._create_user_if_unavailable(
                    email=serializer.validated_data.get("email"),
                    username=serializer.validated_data.get("username"),
                    referral_code=referral_code,
                )
                self.send_welcome_email(user.email)
                return Response(
                    {"message": "User registered successfully."},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                return Response(
                    {"message": "A user with this email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_referrer(self, referral_code: str | None) -> UserObject | None:
        if referral_code:
            try:
                return Profile.objects.get(referral_code=referral_code).user
            except Profile.DoesNotExist:
                pass
        return None

    def _create_user_if_unavailable(
        self, email: str, username: str, referral_code: str | None = None,
    ) -> UserObject:
        with transaction.atomic():
            user = User.objects.create_user(email=email, username=username)
            profile = Profile.objects.get(user=user)
            profile.referred_by = self.get_referrer(referral_code)
            profile.first_name = username
            profile.referral_code = generate_referral_code(profile.pk)
            profile.save()
        return user


class UserTokenValidation(APIView, BuildMagicLink):
    permission_classes = [permissions.AllowAny]
    token = JWTAuthentication()

    def post(self, request, *args, **kwargs):
        user, _ = self.token.authenticate(request)
        if user:
            self.send_login_email(user, "account/dashboard/v1/mails/login.html")
            return Response({"message": "Token is valid", "success": True},status=status.HTTP_200_OK)  # noqa: E501
        return  Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)  # noqa: E501


class ValidateAuthenticatedUserView(APIView):
    permission_classes = [permissions.AllowAny]
    token = JWTAuthentication()
    def post(self, request, *args, **kwargs):
        user, _ = self.token.authenticate(request)
        if user:
            return Response({"message": "Token is valid", "success": True},status=status.HTTP_200_OK)  # noqa: E501
        return Response({}, status.HTTP_400_BAD_REQUEST)


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
