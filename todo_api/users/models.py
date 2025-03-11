from django.contrib.auth.models import User
from django.db import models
from tasks.fields import HashAutoField


class UserProfile(models.Model):
    id = HashAutoField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        help_text="Идентификатор пользователя в Telegram для уведомлений",
    )
    receive_notifications = models.BooleanField(
        default=True, help_text="Получать уведомления?"
    )

    def __str__(self):
        return f"Профиль {self.user.username}"
