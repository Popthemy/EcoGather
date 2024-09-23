from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import URLValidator
# Create your models here.
# Demo models


class BaseSocialMediaLink(models.Model):
    """ Model contains social medial link for each models """

    facebook = models.URLField(
        blank=True, null=True, validators=[URLValidator])
    linkedin = models.URLField(
        blank=True, null=True, validators=[URLValidator])
    youtube = models.URLField(blank=True, null=True, validators=[URLValidator])
    twitter = models.URLField(blank=True, null=True, validators=[URLValidator])
    instagram = models.URLField(
        blank=True, null=True, validators=[URLValidator])
    website = models.URLField(
        blank=True, null=True, validators=[URLValidator])

    class Meta:
        """ The abstract makes this class a base class"""
        abstract = True
        ordering = ['website']

