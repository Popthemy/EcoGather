from django.db import models


class OrganizerManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('user').prefetch_related('addresses')


class AddressManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('organizer')


class ProgramManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('featured_event').prefetch_related('events')


class EventManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('program','organizer').prefetch_related('templates')


class TemplateManager(models.Manager):
    '''Custom manager for template.'''
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('event','owner')

class CustomFieldManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('template')
    }
    
