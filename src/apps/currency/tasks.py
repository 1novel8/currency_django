from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apps.currency.models import Currency

NOTIFICATION_PERIOD = settings.NOTIFICATION_PERIOD
HOST_URL = settings.HOST_URL
HOST_PORT = settings.HOST_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER


@shared_task()
def currency_updated_notification() -> None:
    updated_currencies = (Currency.objects
                          .filter(updated_at__gte=timezone.now() - NOTIFICATION_PERIOD)
                          .prefetch_related('user_subscriptions').all())
    for currency in updated_currencies:
        user_email_list = []
        for user in currency.user_subscriptions.all():
            user_email_list.append(user.email)

        subject = f'Currency {currency.name} updated!'

        currency_url = f'http://{HOST_URL}:{HOST_PORT}/api/currencies/{currency.id}'

        message = f'{currency.name} now:\n' \
                  f'price for buy - {currency.price_for_buy}\n' \
                  f'price for sale - {currency.price_for_sale} \n' \
                  f'{currency_url}'

        from_email = EMAIL_HOST_USER
        to_email_list = user_email_list
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=to_email_list,
            fail_silently=False
        )
