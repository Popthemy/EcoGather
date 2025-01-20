from .common import *
from decouple import config


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('MY_SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware' ] #debug toolbar


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}