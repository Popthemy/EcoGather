from django.contrib.auth import get_user_model

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Organizer
User = get_user_model()


@receiver(post_save, sender=User)
def create_organizer_profile_from_new_user(sender, instance, created, **kwargs):
    """A user sign in and get assigned a profile"""
    if created:
        new_user = instance
        Organizer.objects.create(user=new_user, email=new_user.email)


@receiver(post_save, sender=Organizer)
def update_user_from_organizer_update(sender, instance, created, **kwargs):
    """ To keep a consistent record between user and organizer models we should 
    update this fields when set on the organizer model."""

    if created is False:
        organizer = instance
        user = User.objects.get(pk=instance.pk)
        user.email = organizer.email
        user.first_name = organizer.first_name
        user.last_name = organizer.last_name
        user.save()

@receiver(post_delete,sender=Organizer)
def delete_user_when_organizer_delete(sender,instance,**kwargs):
    """Remove a user along with their profile."""
    
    try:
        user = getattr(instance,'user')
        user.delete()
    except User.DoesNotExist:
        pass