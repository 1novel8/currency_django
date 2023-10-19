import os

from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def send_new_password(new_password: str, email: str) -> None:
    subject = 'Password reset!'

    reset_password_url = 'http://locslhost:8000/api/auth/change_password'

    message = f'Your new password is:\n' \
              f'{new_password}' \
              f'You can change it here:\n' \
              f'{reset_password_url}'

    from_email = os.environ.get("EMAIL_HOST_USER")  # pylint: disable=no-member
    to_email = [email]
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=to_email,
        fail_silently=False
    )