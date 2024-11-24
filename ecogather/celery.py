from celery import Celery
import os

# set default django settings module for celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecogather.settings')

celery = Celery('ecogather') # celery instance

celery.config_from_object('django.conf:settings',namespace='CELERY')

celery.autodiscover_tasks()
