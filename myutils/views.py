from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from greenplan.models import Event, Template, CustomField, Program
# from .seed import user_seed_data , event_seed_data , template_seed_data ,custom_field_seed_data


# Create your views here.

Users = get_user_model()


@api_view(['GET'])
def import_dummy_data(request):
    try:

        # users = [ Users(**user) for user in user_seed_data ]
        # user = Users.objects.bulk_create(users)

        inserted_users = {str(user.id): user for user in Users.objects.all()}

        for event in event_seed_data:

            user_id = str(event['organizer'])
            if user_id in inserted_users:
                print('Found a match inserting')
                event['organizer'] = inserted_users[user_id]
            else:
                print('Did not find a match but i got u,inserting')

        # events = [Event(**event) for event in event_seed_data]
        # event = Event.objects.bulk_create(events)

        # bulletins = [Template(**template)
        #              for template in template_seed_data]
        # bulletin = Template.objects.bulk_create(bulletins)

        # fields = [CustomField(**field) for field in custom_field_seed_data]
        # field = CustomField.objects.bulk_create(fields)

        return Response({'message': "succesfull"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'errors': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


def list_event(request):
    events = Event.objects.select_related('organizer', 'program')
    programs = Program.objects.select_related(
        'featured_event').annotate(event_count=Count("events"))
    
    summit_event = Event.objects.filter(program__title__icontains='summit').values_list('id') # get summit event

    templates = Template.objects.filter(event_name_id__in=summit_event) # .values_list('event_name','event_name__program__title','event_name__title')  # # get template associated to each event

    template_fields = CustomField.objects.select_related('template').filter(template__id__in=templates).order_by('template__id').distinct()

    context = {'events': events, 'programs': programs,'summit_event':summit_event,'templates': templates, 'template_fields': template_fields
              }
    return render(request, 'demo.html', context)
