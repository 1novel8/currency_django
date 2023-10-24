import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # pylint: disable=no-member

app = Celery('celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Minsk'
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'currency-updated-notification': {
        'task': 'apps.currency.tasks.currency_updated_notification',
        'schedule': 300,
    },
}
