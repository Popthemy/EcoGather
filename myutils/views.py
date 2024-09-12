from django.shortcuts import render
from greenplan.models import Event, BulletinTemplate, CustomField
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from .seed import event_seed_data, bulletin_template_seed_data, custom_field_seed_data
from greenplan.models import Event, BulletinTemplate, CustomField


# Create your views here.


@api_view(['GET'])
def import_dummy_data(request):
    try:
        events = [ Event(**event) for event in event_seed_data  ]
        event = Event.objects.bulk_create(events)
        
        bulletins = [BulletinTemplate(**template) for template in bulletin_template_seed_data]
        bulletin = BulletinTemplate.objects.bulk_create(bulletins)
        
        fields = [ CustomField(**field) for field in custom_field_seed_data ]
        field = CustomField.objects.bulk_create(fields)

        return Response({'message': "succesfull"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'errors': f'{str(e)}'},status=status.HTTP_400_BAD_REQUEST)


"""@api_view(['GET'])
def import_dummy_data(request):
    try:
        # Convert dictionaries to Event instances
        event_instances = [Event(**data) for data in event_seed_data]
        Event.objects.bulk_create(event_instances)

        # Convert dictionaries to BulletinTemplate instances
        bulletin_instances = [BulletinTemplate(**data) for data in bulletin_template_seed_data]
        BulletinTemplate.objects.bulk_create(bulletin_instances)

        # Convert dictionaries to CustomField instances
        custom_field_instances = [CustomField(**data) for data in custom_field_seed_data]
        CustomField.objects.bulk_create(custom_field_instances)

        return Response({'message': "successful"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'errors': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
"""