from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from greenplan.admin import EventAdmin, EventImageInline, Event
from sponsors.models import Sponsorship
# Register your models here.


class SponsorshipInline(GenericTabularInline):
    model = Sponsorship
    autocomplete_fields = ['sponsor']


class CustomEventAdmin(EventAdmin):
    inlines = [SponsorshipInline, EventImageInline]


admin.site.unregister(Event)
admin.site.register(Event, CustomEventAdmin)
