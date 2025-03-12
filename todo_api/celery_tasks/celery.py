import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_api.settings')
app = Celery(
    'tasks',
    broker=f'redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0',
    backend=f'redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0',
    include=['celery_tasks.notifications'],
)
app.conf.broker_connection_retry_on_startup = True
app.conf.timezone = settings.TIME_ZONE
app.config_from_object('todo_api.settings', namespace='CELERY')
app.autodiscover_tasks(['celery_tasks'])

app.conf.beat_schedule = {
    "check_due_task_notifications": {
        "task": "celery_tasks.notifications.check_due_tasks",
        "schedule": crontab(hour="12"),
    },
}
