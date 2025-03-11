from django.urls import path
from users.views import (
    TelegramRegisterView,
    TokenObtainPairFromBotView,
    TokenRefreshFromBotView,
)

urlpatterns = [
    path("register/", TelegramRegisterView.as_view(), name="register-telegram"),
    path("token/", TokenObtainPairFromBotView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshFromBotView.as_view(), name="token_refresh"),
]
