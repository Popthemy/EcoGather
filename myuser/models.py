from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from myuser.manager import CustomBaseUserManager
# Create your models here.


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid4,primary_key=True,unique=True,editable=False)
    username = None
    email = models.EmailField(unique=True)
    objects = CustomBaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return self.get_full_name()
