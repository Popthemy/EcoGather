import random
import string
from django.db import models
from django.conf import settings
from django.utils import timezone, text
from django.db import transaction
from django.core.exceptions import ValidationError
# Create your models here.


class Program(models.Model):
    """Categories of event"""

    title = models.CharField(
        max_length=255, help_text='Categories of event e.g Conference,Summit,Webinar')
    featured_event = models.ForeignKey(
        'Event', on_delete=models.SET_NULL, blank=True, null=True, related_name='featured_event')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Event(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Enter a unique code name for this event. e.g ACADA2024."
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    program = models.ForeignKey(
        Program, on_delete=models.PROTECT, related_name='events', null=True)
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True,
                            help_text="A slug is a URL-friendly version of the title. It should contain only letters, numbers, hyphens, and underscores. It will be used in URLs to identify this item."
                            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime', '-updated_at', 'title']

    def clean(self):
        if self.start_datetime > self.end_datetime:
            raise ValidationError(
                'Start date and time should be before End date and time')

        return super().clean()

    def __str__(self):
        return f'{self.code} at {self.location} \
          [{self.start_datetime.strftime("%b %d, %I:%M %p")} - {self.end_datetime.strftime("%b %d, %Y %I:%M %p")}]'

    def get_event_status(self):
        """ Get the status of an event if it is PAST, ONGOING, UPCOMING """
        now = timezone.now()  # Use timezone-aware current time

        if now < self.start_datetime:
            return 'UPCOMING'
        if self.start_datetime <= now <= self.end_datetime:
            return 'ONGOING'
        else:
            return 'PAST'

    def get_organizer_total_events(self):
        return Event.objects.filter(organizer=self.organizer).count()

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = text.slugify(self.title)
            slug = base_slug
            counter = 1
            # Check for slug conflicts and modify the slug if necessary
            while Event.objects.only('slug').filter(slug=slug).exclude(pk=self.pk if self.pk else None).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Template(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Enter a unique code name for this template. \
          Use alphanumeric characters and hyphens."
    )
    title = models.CharField(max_length=255)
    event_name = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='template', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True,
                            help_text="A slug is a URL-friendly version of the title. It should contain only letters, numbers, hyphens, and underscores. It will be used in URLs to identify this item."
                            )
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'title']
        verbose_name = "Template"
        verbose_name_plural = "Templates"

    def __str__(self):
        return f'{self.code} (Event: {self.event_name.title})'

    def generate_unique_code(self):
        '''Generate unique code for event if not set so as to reduce case of integrity error'''
        character = random.choices(string.ascii_uppercase, k=6)
        digit = random.choices(string.digits, k=4)
        code = character + digit
        return ''.join(code)

    def clone(self, new_template=None):

        with transaction.atomic():
            if self.custom_field.exists():
                new_template = Template.objects.create(
                    title=f'{self.title } (copy)',
                    event_name=self.event_name,
                    code=self.generate_unique_code()
                )

                for custom_field in self.custom_field.all():
                    CustomField.objects.create(
                        template=new_template,
                        label=custom_field.label,
                        content=custom_field.content,
                        start_time=custom_field.start_time,
                        end_time=custom_field.end_time

                    )

                return new_template
        return None

    def save(self, *args, **kwargs):
        # If slug is not provided, generate it from the title
        if not self.slug:
            base_slug = text.slugify(self.title)
            slug = base_slug
            counter = 1
            while Template.objects.only('slug').filter(slug=slug).exclude(pk=self.pk if self.pk else None).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Generate a code if it doesn't exist or is duplicated
        if not self.code:
            self.code = self.generate_unique_code()

        # Ensure uniqueness of the code
        while Template.objects.filter(code=self.code).exclude(pk=self.pk if self.pk else None).exists():
            self.code = self.generate_unique_code()

        super().save(*args, **kwargs)


class CustomField(models.Model):

    """Custom Field data sample:

        label: Precensional Hymn EBH 20
        content: Song Lead by the Choir
        Start Time: 7:30 AM
        End Time: 7:50 AM
    """

    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, related_name='custom_field')
    label = models.CharField(max_length=255)
    content = models.TextField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['start_time', 'label']

    def __str__(self):
        start_time = self.start_time.strftime(
            "%I:%M %p") if self.start_time else "No Time"
        end_time = self.end_time.strftime(
            "%I:%M %p") if self.end_time else "No Time"
        return f'{self.label}: {self.content} ({start_time} - {end_time} )'
