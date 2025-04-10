from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tasks.permissions import IsAuthenticatedOrTelegramBot
from users.models import UserProfile

User = get_user_model()


class TelegramRegisterView(APIView):
    """
    API endpoint for registering users via Telegram.

    - Takes `telegram_id` and optional` username`.
    - If the user is not found, creates a new one.
    - If `username` is not conveyed,` user_ {telegram_id} `is used.
    """

    http_method_names = ["post"]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        username = request.data.get("username", f"user_{telegram_id}")

        if not telegram_id:
            return Response(
                {"error": "Missing telegram_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        user, created = User.objects.get_or_create(username=username)
        UserProfile.objects.get_or_create(telegram_chat_id=telegram_id, user=user)

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "telegram_id": user.profile.telegram_chat_id,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class TokenObtainPairFromBotView(TokenObtainPairView):
    """
    API endpoint for a pair of tokens (Access + Refresh) for Telegram Bota.

    - It requires `username` in the body of the request.
    - Returns Access and Refresh tokens if the user exists.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")

        if not username:
            raise AuthenticationFailed("Username is required")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User does not exist")

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})


class TokenRefreshFromBotView(TokenRefreshView):
    """
    API for updating the Access Token via Refresh-Taken.

    - Requires `refresh` in the body of the request.
    - Products a new Access and Refresh tokens.
    """

    permission_classes = (IsAuthenticatedOrTelegramBot,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            raise AuthenticationFailed("Refresh token is required")

        try:
            refresh = RefreshToken(refresh_token)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)}
            )
        except (TokenError, InvalidToken):
            raise AuthenticationFailed("Invalid or expired refresh token")
