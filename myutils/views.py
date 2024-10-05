from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from greenplan.models import Event, Template, CustomField, Program, Organizer
from sponsors.models import Sponsor,Sponsorship
# from .seed import user_seed_data, program_seed_data, organizer_seed_data , event_seed_data, template_seed_data, custom_field_seed_data, sponsors_seed_data

# Create your views here.

Users = get_user_model()


@api_view(['GET'])
def import_dummy_data(request):
    try:
        # insert user
        # users = [ Users(**user) for user in user_seed_data ]
        # user = Users.objects.bulk_create(users)

        # insert programs
        # programs = [Program(**program) for program in program_seed_data]
        # program = Program.objects.bulk_create(programs)

        # insert organizers
        # organizers = [ Organizer(**organizer) for organizer in organizer_seed_data]
        # organizer = Organizer.objects.bulk_create(organizers)

        # insert events
        # events = [Event(**event) for event in event_seed_data]
        # event = Event.objects.bulk_create(events)

        # insert bulletins
        # bulletins = [Template(**template)
        #              for template in template_seed_data]
        # bulletin = Template.objects.bulk_create(bulletins)

        # insert fields
        # fields = [CustomField(**field) for field in custom_field_seed_data]
        # field = CustomField.objects.bulk_create(fields)

        # insert sponsors
        # sponsors = [Sponsor(**sponsor) for sponsor in sponsors_seed_data]
        # sponsor= Sponsor.objects.bulk_create(sponsors)

        return Response({'message': "successful"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'errors': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


def list_event(request):
    events = Event.objects.select_related('organizer', 'program')
    programs = Program.objects.select_related(
        'featured_event').annotate(event_count=Count("events"))

    summit_event = Event.objects.filter(
        program__title__icontains='summit').values_list('id')  # get summit event

    templates = Template.objects.filter(event_name_id__in=summit_event)

    template_fields = CustomField.objects.select_related('template').filter(
        template__id__in=templates).order_by('template__id')


    sponsored_events = Sponsorship.objects.select_related('sponsor').all() #create_sponsors_for(sponsor_name='Culinary Creations',obj_type=Event,obj_id=2) #get_sponsors_for(Event,1)
    
    context = {'events': events, 'programs': programs, 'summit_event': summit_event, \
               'templates': templates, 'template_fields': template_fields, "sponsored_events": sponsored_events
               }
    return render(request, 'demo.html', context)
