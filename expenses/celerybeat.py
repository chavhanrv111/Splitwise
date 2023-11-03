from celery import Celery
from celery.schedules import crontab

app = Celery('sw')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send-weekly-balance-email': {
        'task': 'expenses.tasks.send_weekly_balance_email',
        'schedule': crontab(day_of_week=0, hour=0, minute=0),  # Adjust the schedule as needed
    },
}


# celery -A sw worker --loglevel=info
# celery -A sw beat --loglevel=info