import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv  # pylint: disable=import-error

load_dotenv()  # load .env

NOTIFICATION_PERIOD = timedelta(minutes=5)
HOST_URL = os.getenv('DJANGO_HOST')  # pylint: disable=no-member
HOST_PORT = os.getenv('DJANGO_PORT')  # pylint: disable=no-member

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')  # pylint: disable=no-member

DEBUG = True

AUTH_USER_MODEL = 'user.User'

ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'storages',

    'apps.authentication.apps.AuthenticationConfig',
    'apps.user.apps.UserConfig',
    'apps.currency.apps.CurrencyConfig',
    'apps.order.apps.OrderConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),  # pylint: disable=no-member
        'USER': os.getenv('POSTGRES_USER'),  # pylint: disable=no-member
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),  # pylint: disable=no-member
        'HOST': os.getenv('POSTGRES_HOST'),  # pylint: disable=no-member
        'PORT': os.getenv('POSTGRES_PORT'),  # pylint: disable=no-member
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_TEST_NAME'),  # pylint: disable=no-member
        'USER': os.getenv('POSTGRES_USER'),  # pylint: disable=no-member
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),  # pylint: disable=no-member
        'HOST': os.getenv('POSTGRES_HOST'),  # pylint: disable=no-member
        'PORT': os.getenv('POSTGRES_PORT'),  # pylint: disable=no-member
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.authentication.authentication_classes.JWTAuthentication',
    )
}

JWT = {
    'TOKEN_EXPIRE': timedelta(days=1),
}

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER")  # pylint: disable=no-member
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER")  # pylint: disable=no-member

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")  # pylint: disable=no-member
EMAIL_PORT = os.environ.get("EMAIL_PORT")  # pylint: disable=no-member
EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")  # pylint: disable=no-member
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")  # pylint: disable=no-member

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')  # pylint: disable=no-member
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')  # pylint: disable=no-member
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')  # pylint: disable=no-member
LOCALSTACK_PORT = os.getenv('LOCALSTACK_PORT')  # pylint: disable=no-member
AWS_S3_ENDPOINT_URL = f'{os.getenv("AWS_S3_ENDPOINT_URL")}:{os.getenv("LOCALSTACK_PORT")}'  # pylint: disable=no-member
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')  # pylint: disable=no-member
AWS_DEFAULT_ACL = os.getenv('AWS_DEFAULT_ACL')  # pylint: disable=no-member

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
