from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from sponsors.models import Sponsor,Sponsorship

# Register your models here.


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    search_fields = ['name']

    class Meta:
        model = Sponsor
        fields = '__all__'


    list_display = [ 'name','email', 'sponsored_count' ,'description' ]

    @admin.display(ordering='total_sponsored_count')
    def sponsored_count(self,sponsor):
        return sponsor.total_sponsored_count
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.annotate(total_sponsored_count=Count('sponsors'))


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    fields = ['sponsor','content_type','object_id']

    list_display =  ['id','sponsor','content_type','object_id','content_object']

