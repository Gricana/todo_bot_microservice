import asyncio
import logging

import httpx
import pytz
from celery import shared_task
from celery_tasks.utils import send_telegram_message
from django.utils import timezone
from tasks.models import Task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(name="celery_tasks.notifications.check_due_tasks")
def check_due_tasks():
    """
    Checks the tasks with the next term of execution and plans notifications.
    """
    msk_tz = pytz.timezone('Europe/Moscow')
    now = timezone.now()
    due_tasks = Task.objects.filter(status=Task.Status.TODO, due_date__date=now.date())
    for task in due_tasks:
        task_time = task.due_date.astimezone(msk_tz)
        send_task_notification.apply_async((task.id,), eta=task_time)


@shared_task(bind=True, max_retries=3, retry_backoff=True)
def send_task_notification(self, task_id):
    """
    Sends a notice to Telegram about the task with the approaching deadline.
    """
    try:
        task = Task.objects.get(id=task_id)
        user_profile = task.user.profile

        if user_profile.receive_notifications and user_profile.telegram_chat_id:
            due_date_user_tz = task.due_date.astimezone(pytz.timezone("Europe/Moscow"))
            message = f"🔔 Напоминание: <a href='https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start=task_{task.id}'>{task.title}</a>\n⏳ Дедлайн: {due_date_user_tz.strftime('%d.%m.%Y %H:%M')}"
            asyncio.run(send_telegram_message(user_profile.telegram_chat_id, message))

    except Task.DoesNotExist:
        logger.warning(f"Задача {task_id} не найдена.")
    except httpx.RequestError as exc:
        logger.error(f"Ошибка сети для задачи {task_id}: {exc}")
        raise self.retry(exc=exc)
    except Exception as exc:
        logger.error(f"Ошибка уведомления: {exc}")
        raise self.retry(exc=exc)
