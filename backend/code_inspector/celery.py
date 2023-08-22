import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_inspector.settings')

app = Celery('code_inspector')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_code_report_every_1_minutes': {
        'task': 'users.tasks.send_report',
        'schedule': crontab(minute='*/1')
    }
}
