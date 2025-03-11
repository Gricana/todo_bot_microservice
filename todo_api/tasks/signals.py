from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from tasks.models import Task


def reset_cache(user_id):
    """
    Removes the cache of the task list for the specified user.

    Param User_id: ID of the user for whom you need to clean the cache.
    """
    cache.delete(settings.TASK_CACHE_KEY.format(user_id=user_id))


@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def clear_task_cache(sender, instance, **kwargs):
    """
    Cleans the user's quest to create, update or delete the task.

    It is called automatically when the signals are triggered `post_save` and` post_delete`.
    """
    reset_cache(instance.user.id)
