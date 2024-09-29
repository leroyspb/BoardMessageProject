import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mes_board.settings')

app = Celery('mes_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'board.tasks.send_mail_monday_8am',
        'schedule': crontab(hour=22, minute=9, day_of_week='sunday'),
        'args': (20,),

        # crontab(hour=8, minute=0, day_of_week='monday'),
        # crontab(hour=21, minute=50, day_of_week='sunday'),
    },
}
