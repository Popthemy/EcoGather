import random
import string
from django.db import models
from django.conf import settings
from django.utils import timezone, text
from django.db import transaction
from django.core.exceptions import ValidationError
from myutils.models import BaseSocialMediaLink
from .managers import OrganizerManager, AddressManager, EventManager
# Create your models here.



class Organizer(BaseSocialMediaLink):
    """ Similar to the profile model in apps"""

    INDIVIDUAL_TYPE = "INDIVIDUAL"
    ORGANIZATION_TYPE = 'ORGANIZATION'

    ORGANIZER_TYPES = (
        (INDIVIDUAL_TYPE, 'Individual'),
        (ORGANIZATION_TYPE, 'Organization'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    type = models.TextField(
        max_length=30, choices=ORGANIZER_TYPES, default=INDIVIDUAL_TYPE)
    bio = models.TextField(null=True, blank=True)
    vision = models.CharField(max_length=255, null=True, blank=True)
    mission = models.CharField(max_length=255, null=True, blank=True)
    objects = OrganizerManager()

    class Meta:
        ordering = ['username', 'first_name', 'last_name', 'type']
        verbose_name = 'Organizer'
        verbose_name_plural = 'Organizers'

    def __str__(self) -> str:
        return f"{self.username} - {self.phone_number}"

    def get_organizer_total_events(self):
        ''' Count the number of time an organizer has organized an event'''
        return self.organizer.count()

class OrganizerImage(models.Model):
    MAIN ='MAIN'
    SUB = "SUB"
    NEUTRAL = "SUB"

    IMAGE_CHOICE =(
        (MAIN,'main'),(SUB,'sub'), (NEUTRAL,'neutral')
    )

    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE,related_name='images')
    image_url = models.ImageField(null=True,blank=True,upload_to='organizers/',default='default_organizer.png')
    type = models.CharField( max_length=20,choices=IMAGE_CHOICE,default=NEUTRAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['type','updated_at','organizer']

    def save(self,*args, **kwargs):
        if self.image_url == '':
            self.image_url = 'default_organizer.png'
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return f"{self.organizer.username} {self.type} image"


class Address(models.Model):
    'address for each organizer, an organizer might have more than one address'

    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, related_name='addresses')
    street_number = models.PositiveIntegerField()
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=255)
    objects = AddressManager()

    class Meta:
        ordering = ['street_number', 'street_name', 'city', 'zip_code']
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self) -> str:
        return f'{self.organizer} reside at {self.street_number} {self.street_name},{self.city},{self.state}'


class Program(models.Model):
    """Categories of event e.g summit, conference"""

    title = models.CharField(
        max_length=255, unique=True, help_text='Categories of event e.g Conference,Summit,Webinar')
    featured_event = models.ForeignKey(
        'Event', on_delete=models.SET_NULL, blank=True, null=True, related_name='featured_event')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'


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
    venue = models.CharField(max_length=255,help_text="Exact location where the event is taking place e.g The Great hall,Lautech")
    city = models.CharField(max_length=255,help_text="City or state the event could be taking place e.g Ogbomoso")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, related_name='organizer')
    slug = models.SlugField(unique=True, blank=True, null=True,
                            help_text="A slug is a URL-friendly version of the title. It should contain only letters, numbers, hyphens, and underscores. It will be used in URLs to identify this item."
                            )
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()

    class Meta:
        ordering = ['start_datetime', '-updated_at', 'title']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def clean(self):
        if self.start_datetime > self.end_datetime:
            raise ValidationError(
                'Start date and time should be before End date and time')
        return super().clean()

    def __str__(self):
        return f'{self.code} at {self.venue} \
          [{self.start_datetime.strftime("%b %d, %I:%M %p")} - {self.end_datetime.strftime("%b %d, %Y %I:%M %p")}]'

    def get_event_status(self):
        """ Get the status of an event if it is PAST, ONGOING, UPCOMING """
        now = timezone.now()  # Use timezone-aware current time

        if now < self.start_datetime:
            return 'UPCOMING'
        if self.start_datetime <= now <= self.end_datetime:
            return 'ONGOING'
        return 'PAST'

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
    owner = models.ForeignKey(
        Organizer,on_delete=models.CASCADE, related_name='template_owner')

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Enter a unique code name for this template. \
          Use alphanumeric characters and hyphens."
    )
    title = models.CharField(max_length=255)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='templates', null=True, blank=True)
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
        return f'{self.code} (Event: {self.event.title if self.event else None})'

    def generate_unique_code(self):
        '''Generate unique code for event if not set so as to reduce case of integrity error'''
        character = random.choices(string.ascii_uppercase, k=6)
        digit = random.choices(string.digits, k=4)
        code = character + digit
        return ''.join(code)

    def clone(self,user, new_template=None):
        '''This help template to be reused, user an decide to clone their template 
        or another users template provided it is available.'''

        with transaction.atomic():
            if self.custom_fields.exists():
                new_template = Template.objects.create(
                    title=f'{self.title } (cloned)',
                    event=None,
                    owner=user,
                    code=self.generate_unique_code()
                )

                custom_fields = [CustomField(
                    template=new_template,
                    label=field.label,
                    content=field.content,
                    start_time=field.start_time,
                    end_time=field.end_time)
                    for field in self.custom_fields.all()]

                CustomField.objects.bulk_create(custom_fields)
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

        label: Precessional Hymn EBH 20
        content: Song Lead by the Choir
        Start Time: 7:30 AM
        End Time: 7:50 AM
    """

    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, related_name='custom_fields')
    label = models.CharField(max_length=255)
    content = models.TextField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ['start_time', 'label']
        verbose_name = 'Custom Field'
        verbose_name_plural = 'Custom Fields'

    def __str__(self):
        start_time = self.start_time.strftime(
            "%I:%M %p") if self.start_time else "No Time"
        end_time = self.end_time.strftime(
            "%I:%M %p") if self.end_time else "No Time"
        return f'{self.label}: {self.content} ({start_time} - {end_time} )'
