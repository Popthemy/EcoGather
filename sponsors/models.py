from django.db import models
from django.core.validators import URLValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from myutils.models import BaseSocialMediaLink
# Create your models here.


class SponsorshipManager(models.Manager):

    def get_sponsors_for(self, obj_type, obj_id):
        '''Obj_type: a model e.g event
        obj_id: the id of the referenced item on the table'''

        content_type = ContentType.objects.get_for_model(obj_type)

        return Sponsorship.objects.select_related('sponsor').filter(
            content_type=content_type,
            object_id=obj_id
        )

    def create_sponsors_for(self, sponsor_name, obj_type, obj_id):
        '''Obj_type: a model e.g event
        obj_id: the id of the referenced item on the table'''

        sponsor_instance = Sponsor.objects.get(name=sponsor_name)

        content_type = ContentType.objects.get_for_model(obj_type)

        return Sponsorship.objects.create(
            sponsor=sponsor_instance,
            content_type=content_type,
            object_id=obj_id
        )


class Sponsor(BaseSocialMediaLink):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsors'

    def __str__(self) -> str:
        return self.name

    def get_total_sponsored_event(self):
        '''Count the total number of event sponsored by the sponsor'''
        qs = Sponsor.objects.filter(name=self.name).annotate(total_sponsored_count=models.aggregates.Count('sponsors')).order_by('total_sponsored_count').first()
        return qs.total_sponsored_count


class Sponsorship(models.Model):
    """ What is been sponsored by which sponsor"""
    objects = SponsorshipManager()
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.CASCADE, related_name='sponsors')

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)  # model
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        ordering = ['sponsor']
        verbose_name= 'Sponsorship' 
        verbose_name_plural= 'Sponsorships' 

    def __str__(self) -> str:
        return f'{self.sponsor} sponsors {self.content_object}'
