from os import environ, urandom

from backend.settings.common import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('POSTGRES_DB', 'postgres'),
        'USER': environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': 'db',
        'PORT': '5432'
    }
}

SECRET_KEY = urandom(16).hex()

DEBUG = False

STATIC_ROOT = BASE_DIR / 'staticfiles'
