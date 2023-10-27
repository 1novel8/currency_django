import os

import boto3
from django.conf import settings

EMAIL_HOST_USER = settings.EMAIL_HOST_USER
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')  # pylint: disable=no-member
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')  # pylint: disable=no-member
LOCALSTACK_PORT = os.getenv('LOCALSTACK_PORT')  # pylint: disable=no-member

ses_client = boto3.client(
    'ses',
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    region_name='us-east-1',
    endpoint_url=f'http://host.docker.internal:{LOCALSTACK_PORT}'
)
ses_client.verify_email_identity(EmailAddress=EMAIL_HOST_USER)
