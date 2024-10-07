from django.utils import timezone
from celery import shared_task
from trackers.models import Task
from trackers.services import create_telegram_message


@shared_task
def reminder():
    """Отложенная задача Celery для напоминания о выполнении задачи"""

    now = timezone.now()
    tasks = Task.objects.filter(status="ToDo").exclude(executor__chat_id=None)
    for task in tasks:
        if task.start_execution <= now <= task.time_complete:
            create_telegram_message(task)
