import random
import string
from django.db import models
from django.conf import settings
from django.utils import timezone, text

# Create your models here.


class Event(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Enter a unique code name for this event. e.g ACADA2024."
    )
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return f'Event: {self.code} at {self.location} \
          [{self.start_time.strftime("%b %d, %Y %I:%M %p")}]'

    def get_event_status(self):
        """ Get when and event is happening"""
        now = timezone.now()  # Use timezone-aware current time

        if not self.start_time or not self.end_time:
            return 'UNKNOWN'

        if now < self.start_time:
            return 'UPCOMING'
        elif self.start_time <= now <= self.end_time:
            return 'ONGOING'
        else:
            return 'PAST'

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = text.slugify(self.title)
            slug = base_slug
            counter = 1
            # Check for slug conflicts and modify the slug if necessary
            while Event.objects.only('slug').filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class BulletinTemplate(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Enter a unique code name for this template. \
          Use alphanumeric characters and hyphens."
    )
    title = models.CharField(max_length=255)
    event_name = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='bulletin', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Bulletin Template"
        verbose_name_plural = "Bulletin Templates"

    def __str__(self):
        return f'Template: {self.code} (Event: {self.event_name.title})'

    def generate_unique_code(self):
        '''Generate unique code for event if not set so as to reduce case of integrity error'''
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def clone(self, new_template=None):

        if self.custom_field.exists():
            new_template = BulletinTemplate.objects.create(
                title=f'{self.title } (copy)',
                event_name=self.event_name,
                code=self.generate_unique_code()
            )

            for custom_field in self.custom_field.all():
                CustomField.objects.create(
                    bulletin_template=new_template,
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
            while BulletinTemplate.objects.only('slug').filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Generate a code if it doesn't exist or is duplicated
        if not self.code:
            self.code = self.generate_unique_code()

        # Ensure uniqueness of the code
        while BulletinTemplate.objects.filter(code=self.code).exists():
            self.code = self.generate_unique_code()

        super().save(*args, **kwargs)


class CustomField(models.Model):

    """Custom Field data sample:

        label: Precensional Hymn EBH 20
        content: Song Lead by the Choir
        Start Time: 7:30 AM
        End Time: 7:50 AM
    """

    bulletin_template = models.ForeignKey(
        BulletinTemplate, on_delete=models.CASCADE, related_name='custom_field')
    label = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        start_time = self.start_time.strftime(
            "%I:%M %p") if self.start_time else "No Time"
        end_time = self.end_time.strftime(
            "%I:%M %p") if self.end_time else "No Time"
        return f'{self.label}: {self.content} ({start_time} - {end_time} )'
