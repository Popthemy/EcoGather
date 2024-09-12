from django.contrib import admin,messages
from greenplan.models import Event,BulletinTemplate,CustomField
# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ['code','title','slug', 'organizer','start_time', 'end_time', 'location']


class CustomFieldInline(admin.TabularInline):
    model = CustomField


@admin.register(BulletinTemplate)
class BulletinTemplateAdmin(admin.ModelAdmin):
    actions = ['clone_bulletin_template']
    fields = ['code','title','slug', 'event_name', 'description']
    inlines = [CustomFieldInline]

    @admin.action(description='Clone template')
    def clone_bulletin_template(self, request, queryset):
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
                        f'{new_template.template_title} template was successfully cloned!',
                        messages.INFO
                    )
                else:
                    self.message_user(
                        request,
                        f'{template.template_title} is an empty template and was not cloned.',
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
    class Meta:
        model = CustomField
        fields = '__all__'
    # fields = ['bulletin_template', 'label',
    #           'content', 'start_time', 'end_time']

    # list_display = ['bulletin_template', 'label',
    #                 'content', 'start_time', 'end_time']
