from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

HOST_URL = settings.HOST_URL
HOST_PORT = settings.HOST_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER


@shared_task(queue='email')
def send_new_password(new_password: str, email: str) -> None:
    subject = 'Password reset!'

    reset_password_url = f'http://{HOST_URL}:{HOST_PORT}/api/auth/change_password'

    message = f'Your new password is:\n' \
              f'{new_password}\n' \
              f'You can change it here:\n' \
              f'{reset_password_url}'

    from_email = EMAIL_HOST_USER
    to_email = [email]
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=to_email,
        fail_silently=False
    )
