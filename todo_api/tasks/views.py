import logging

from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from tasks.models import Category, Task
from tasks.permissions import IsAuthenticatedOrTelegramBot
from tasks.serializers import CategorySerializer, TaskSerializer

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage user tasks.

    - Uses JWT authentication and custom-made access rights.
    - Caches the list of tasks to increase performance.
    - Supports CRUD operations.
    """

    serializer_class = TaskSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticatedOrTelegramBot]

    def get_queryset(self):
        """
        Receives a cache list of user tasks.
        If there is no cache, it loads from the database, cachs and returns.

        :return: Queryset User Tasks
        """
        user_id = self.request.user.id
        cache_key = settings.TASK_CACHE_KEY.format(user_id=user_id)
        cached_tasks = cache.get(cache_key)

        if cached_tasks is None:
            cached_tasks = Task.objects.filter(user=user_id).prefetch_related(
                Prefetch("categories", queryset=Category.objects.only("id", "name"))
            )
            cache.set(cache_key, cached_tasks, timeout=settings.TASK_CACHE_TIMEOUT)

        return cached_tasks

    def list(self, request, *args, **kwargs):
        """
        Returns a list of user tasks.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"tasks": serializer.data})


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing categories of tasks.

    - Supports standard CRUD operations.
    - Access is limited by authenticated users and Telegram bots.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrTelegramBot]
