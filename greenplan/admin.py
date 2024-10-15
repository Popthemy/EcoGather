from typing import Any
from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from django.utils.html import format_html, urlencode
from django.urls import reverse
from greenplan.models import Event, Template, CustomField, Program, Organizer,Address
# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    fields= ('organizer','street_number','street_name','city','state','zip_code','country')
    list_display = ('id','organizer','street_number','street_name','city','state','country')
    search_fields = ('city','state','country')


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):

    class Meta:
        model = Organizer
        fields = "__all__"


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):

    fields = ['title', 'featured_event']
    list_display = ['title', 'featured_event', 'event_count']
    list_select_related = ['featured_event']
    search_fields = ['title__icontains']

    @admin.display(ordering='event_count')
    def event_count(self, program):
        page_link = reverse('admin:greenplan_event_changelist')
        query_link = (page_link
                      + '?'
                      + urlencode({
                          "program__id": str(program.id)
                      })
                      )
        link_event_count = (
            format_html("<a href='{}'> {} </a>",
                        query_link, program.event_count)
        )
        return link_event_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(event_count=Count('events'))


class EventStatusFilter(admin.SimpleListFilter):
    title = 'event_status'
    parameter_name = 'event_status'
    filter_by_upcoming = 'UPCOMING'
    filter_by_ongoing = 'ONGOING'
    filter_by_past = 'PAST'

    def lookups(self, request, model_admin):
        return [(self.filter_by_upcoming, 'Upcoming'),
                (self.filter_by_ongoing, 'Ongoing'),
                (self.filter_by_past, 'past')]

    def queryset(self, request, queryset):
        cur_date = timezone.now()

        if self.value() == self.filter_by_upcoming:
            return queryset.filter(start_datetime__gt=cur_date)
        if self.value() == self.filter_by_past:
            return queryset.filter(end_datetime__lt=cur_date)
        if self.value() == self.filter_by_ongoing:
            return queryset.filter(start_datetime__lte=cur_date, end_datetime__gte=cur_date)
        return queryset


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ['program']
    prepopulated_fields = {'slug': ['title','code']}
    fields = ['id','code', 'title',  'organizer', 'slug', 'program','is_private', 'description',
              'start_datetime', 'end_datetime', 'venue', 'contact_email', 'contact_phone_number']
    list_display = [ 'code', 'title', 'organizer', 'event_status', 'program','is_private',
                    'venue', 'start_datetime', 'end_datetime']
    list_editable = ['title', 'organizer','is_private', 'venue']
    list_filter = [EventStatusFilter, 'program']
    list_select_related = ['organizer', 'program']
    search_fields = ['code', 'title']
    readonly_fields = ('id',)

    @admin.display(ordering='start_datetime')
    def event_status(self, event):
        return event.get_event_status()



class CustomFieldInline(admin.TabularInline):
    '''Making sure a template have at least 1 field'''
    model = CustomField
    min_num = 1



@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    actions = ['clone_template']
    fields = ['code', 'title', 'event', 'slug', 'description']
    inlines = [CustomFieldInline]
    list_display = ['code', 'title', 'event', 'description']
    list_editable = ['title']
    list_select_related = ['event']

    @admin.action(description='Clone template')
    def clone_template(self, request, queryset):
        """Using the action to clone a template, but empty template can't be cloned"""

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
