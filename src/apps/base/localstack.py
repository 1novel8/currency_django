import json

import boto3
from django.conf import settings

EMAIL_HOST_USER = settings.EMAIL_HOST_USER
AWS_DEFAULT_REGION = settings.AWS_DEFAULT_REGION
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
LOCALSTACK_PORT = settings.LOCALSTACK_PORT
AWS_S3_ENDPOINT_URL = settings.AWS_S3_ENDPOINT_URL
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

ses_client = boto3.client(
    'ses',
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    region_name=AWS_DEFAULT_REGION,
    endpoint_url=f'{AWS_S3_ENDPOINT_URL}:{LOCALSTACK_PORT}'
)
ses_client.verify_email_identity(EmailAddress=EMAIL_HOST_USER)

s3_client = boto3.client(
    "s3",
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    region_name=AWS_DEFAULT_REGION,
    endpoint_url=f'{AWS_S3_ENDPOINT_URL}:{LOCALSTACK_PORT}'
)

s3_client.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": [
                "arn:aws:s3:::images/*"
            ]
        }
    ]
}
s3_client.put_bucket_policy(Bucket=AWS_STORAGE_BUCKET_NAME, Policy=json.dumps(bucket_policy))
