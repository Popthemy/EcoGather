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


from myuser.models import CustomUser
from greenplan.models import Organizer, Program, Event, Template,CustomField,EventComment
from datetime import datetime


# 1. Insert Programs
program_map = {}
for program_data in programs:
    program, created = Program.objects.get_or_create(title=program_data["title"])
    program_map[program_data["title"]] = program

# 2. Insert Organizers
organizer_map = {}
for event_data in events:
    organizer_name = event_data["organizer_name"]
    organizer, created = Organizer.objects.get_or_create(name=organizer_name)
    organizer_map[organizer_name] = organizer

# 3. Insert Events
event_map = {}
for event_data in events:
    program = program_map[event_data["program_title"]]
    organizer = organizer_map[event_data["organizer_name"]]
    event, created = Event.objects.get_or_create(
        title=event_data["title"],
        defaults={
            "program": program,
            "impressions": event_data["impressions"],
            "venue": event_data["venue"],
            "city": event_data["city"],
            "start_datetime": datetime.strptime(event_data["start_datetime"], "%Y-%m-%d %H:%M:%S"),
            "end_datetime": datetime.strptime(event_data["end_datetime"], "%Y-%m-%d %H:%M:%S"),
            "contact_email": event_data["contact_email"],
            "contact_phone_number": event_data["contact_phone_number"],
            "organizer": organizer,
            "slug": event_data["slug"],
            "is_private": event_data["is_private"]
        }
    )
    event_map[event_data["slug"]] = event

# 4. Insert Templates
for template_data in templates:
    event = event_map[template_data["event_slug"]]
    Template.objects.get_or_create(
        title=template_data["title"],
        event=event,
        defaults={"description": template_data["description"]}
    )



print("Data inserted successfully!")
