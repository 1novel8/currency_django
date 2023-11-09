import os

from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # pylint: disable=no-member

app = Celery('celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Minsk'
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('email',  Exchange('email'),   routing_key='email'),
    Queue('orders',  Exchange('orders'),   routing_key='orders'),
    Queue('currency', Exchange('currency'), routing_key='currency'),
)

app.conf.beat_schedule = {
    'receive-updated-currencies': {
        'task': 'apps.currency.tasks.receive_updated_currencies',
        'schedule': 300,
    }
}
