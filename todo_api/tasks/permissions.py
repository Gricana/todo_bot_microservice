from django.conf import settings
from rest_framework.permissions import BasePermission


class IsAuthenticatedOrTelegramBot(BasePermission):
    """
    Castom permission to access the API.

    Access is allowed if:
    - The user is authenticated (regular request).
    - The request contains the correct Telegram Bot API Secret token in the header.
    """

    def has_permission(self, request, view):
        """
        Checks whether the user or bot has access to the resource.

        Returns:
            Bool: True, if access is allowed, otherwise false.
        """
        tg_token = request.headers.get("x-telegram-bot-api-secret-token")
        if tg_token and tg_token in settings.TELEGRAM_SECRET_TOKENS:
            return True

        return bool(request.user and request.user.is_authenticated)
