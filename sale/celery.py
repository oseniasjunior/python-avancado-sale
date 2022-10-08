from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sale.settings')

TASKS = {
    'schedule_task': {
        'task': 'core.tasks.schedule_task',
        'schedule': 5
        # 'schedule': crontab(hour=10, day_of_month='*')
    }
}

app = Celery('sale')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('periodic', Exchange('periodic'), routing_key='periodic'),
)
app.autodiscover_tasks()
app.conf.timezone = 'UTC'
app.conf.beat_schedule = TASKS
