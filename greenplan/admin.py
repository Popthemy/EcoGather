from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.http import HttpRequest
from django.utils import timezone
from greenplan.models import Event, Template, CustomField, Program
# Register your models here.


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):

    fields = ['title', 'featured_event']
    list_display = ['title', 'featured_event', 'event_count']
    list_select_related = ['featured_event']
    search_fields = ['title']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(event_count=Count('events'))

    @admin.display(ordering='event_count')
    def event_count(self, program):
        return program.event_count


class EventStatusFilter(admin.SimpleListFilter):
    title = 'event_status'
    parameter_name = 'event_status'

    def lookups(self, request, model_admin):
        return [('upcoming', 'UPCOMING'), ('ongoing', 'ONGOING'), ('past', 'PAST')]

    def queryset(self, request, queryset):
        cur_date = timezone.now()

        if self.value() == 'upcoming':
            return queryset.filter(start_datetime__gt=cur_date)
        if self.value() == 'past':
            return queryset.filter(end_datetime__lt=cur_date)
        if self.value() == 'ongoing':
            return queryset.filter(start_datetime__lte=cur_date, end_datetime__gte=cur_date)
        return queryset


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ['program']
    prepopulated_fields = {'slug':['title']}
    list_filter = [EventStatusFilter]
    fields = ['code', 'title',  'organizer', 'slug', 'program', 'description',
              'start_datetime', 'end_datetime', 'location', 'contact_email', 'contact_phone_number']

    list_display = ['code', 'title', 'organizer', 'event_status', 'program',
                    'location', 'start_datetime', 'end_datetime']
    list_editable = ['title', 'organizer', 'location']
    list_select_related = ['organizer','program']

    @admin.display(ordering='start_datetime')
    def event_status(self, event):
        return event.get_event_status()


class CustomFieldInline(admin.TabularInline):
    model = CustomField


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    actions = ['clone_template']
    fields = ['code', 'title', 'event_name', 'slug', 'description']
    inlines = [CustomFieldInline]
    list_display = ['code', 'title', 'event_name', 'description']
    list_editable = ['title']
    list_select_related = ['event_name']

    @admin.action(description='Clone template')
    def clone_template(self, request, queryset):
        """Using the action as part of action on the admin panel to clone a template"""

        if queryset.exists():
            cloned_templates = []
            for template in queryset:
                # Ensure that the template has custom fields before cloning
                if template.custom_field.exists():
                    new_template = template.clone()
                    cloned_templates.append(new_template)
                    self.message_user(
                        request,
                        f'{new_template.title} template was successfully cloned!',
                        messages.INFO
                    )
                else:
                    self.message_user(
                        request,
                        f'{template.title} is an empty template and was not cloned.',
                        messages.ERROR
                    )
            if not cloned_templates:
                self.message_user(
                    request,
                    'No templates were cloned due to being empty!',
                    messages.ERROR
                )
        else:
            self.message_user(
                request,
                'No templates selected for cloning.',
                messages.ERROR
            )


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    fields = ['template', 'label',
              'content', 'start_time', 'end_time']

    list_display = ['template', 'label',
                    'content', 'start_time', 'end_time']

    list_editable = ['label', 'content', 'start_time', 'end_time']
    list_select_related = ['template']
