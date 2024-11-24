from celery import shared_task
from time import sleep
from .models import Organizer


@shared_task
def all_event_organizer_email():
    print(' GETTING THE TASK TO COMPARE EMAIL OF USER')
    sleep(20)
    email = Organizer.objects.values('email','user__email')
    sleep(30)
    print('I HAVE GOTTEN THE EMAILS')
    print(email)
  