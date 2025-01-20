'''
The settings have been partitioned into 3 parts 
1. common: contain setting general to our project in all environment
2. prod.py: contain settings for production include constant such as SECRET_KEY, ALLOWED_HOST,DATABASE ,DEBUG
3. dev.py: contain settings for development used locally. this is the default settings
DEBUG = True

'''

from decouple import config
from .common import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('MY_SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('IS_DEBUG',default=False, cast=bool)

ALLOWED_HOSTS = ['.vercel.app', '.now.sh']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}