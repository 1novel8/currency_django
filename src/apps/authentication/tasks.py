from celery import shared_task
from django.conf import settings

from apps.base.localstack import ses_client

HOST_URL = settings.HOST_URL
HOST_PORT = settings.HOST_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER


@shared_task()
def send_new_password(new_password: str, email: str) -> None:
    subject = 'Password reset!'

    reset_password_url = f'http://{HOST_URL}:{HOST_PORT}/api/auth/change_password'

    message = f'Your new password is:\n' \
              f'{new_password}\n' \
              f'You can change it here:\n' \
              f'{reset_password_url}'

    from_email = EMAIL_HOST_USER
    to_email_list = [email]

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
