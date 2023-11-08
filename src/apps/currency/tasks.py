import json

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from kafka import KafkaConsumer

from apps.base.exceptions import NotFound
from apps.base.localstack import ses_client
from apps.currency.models import Currency
from apps.currency.serializers import CurrencyUpdateSerializer
from apps.currency.services import CurrencyService
from apps.order.tasks import check_orders

NOTIFICATION_PERIOD = settings.NOTIFICATION_PERIOD
HOST_URL = settings.HOST_URL
HOST_PORT = settings.HOST_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER


@shared_task(queue='currency')
def currency_updated_notification() -> None:
    updated_currencies = (Currency.objects
                          .filter(updated_at__gte=timezone.now() - NOTIFICATION_PERIOD)
                          .prefetch_related('user_subscriptions').all())
    for currency in updated_currencies:
        user_email_list = []
        for user in currency.user_subscriptions.all():
            user_email_list.append(user.email)
        if len(user_email_list) == 0:
            continue

        subject = f'Currency {currency.name} updated!'

        currency_url = f'http://{HOST_URL}:{HOST_PORT}/api/currencies/{currency.id}'

        message = f'{currency.name} now:\n' \
                  f'price for buy - {currency.price_for_buy}\n' \
                  f'price for sale - {currency.price_for_sale} \n' \
                  f'{currency_url}'

        from_email = EMAIL_HOST_USER
        to_email_list = user_email_list
        ses_client.send_email(
            Source=from_email,
            Destination={
                'ToAddresses': to_email_list,
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': message,
                    },
                },
            }
        )

    check_orders.delay()


@shared_task(queue='currency')
def receive_updated_currencies() -> None:
    consumer = KafkaConsumer(
        'update_currencies',
        bootstrap_servers=settings.KAFKA_URL,
        consumer_timeout_ms=5000,
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    service = CurrencyService()
    for message in consumer:
        data = message.value
        serializer = CurrencyUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            service.update_price(**serializer.validated_data)
        except NotFound:
            continue

    currency_updated_notification.delay()
