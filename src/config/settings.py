import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv  # pylint: disable=import-error

load_dotenv()  # load .env

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
    'apps.authentication.middlewares.JWTMiddleware',
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
    ]
}

JWT = {
    'TOKEN_EXPIRE': timedelta(days=1),
}

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER")  # pylint: disable=no-member
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER")  # pylint: disable=no-member

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")  # pylint: disable=no-member
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")  # pylint: disable=no-member

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
