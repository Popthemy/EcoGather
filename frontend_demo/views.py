from django.shortcuts import render
from greenplan.models import Event, Template,Program
# Create your views here.


""" Include page in every view context data so we can track the page you are currently working on from the title of the HTML page.
e.g {"page":"Event"}
"""

def index(request):
    '''
    Include the events and the program we have. 
    Used featured event image as the program image  '''

    filter_by_program_title = request.GET.get('program',None)

    if filter_by_program_title:
        events = Event.objects.prefetch_related('images').filter(program__title=filter_by_program_title)
    else:
        events = Event.objects.prefetch_related('images').all()

    programs = Program.objects.select_related('featured_event').prefetch_related('featured_event__images').all()

    context = {'page': 'Home page', 'events': events,'programs':programs}
    return render(request, 'frontend_demo/events.html', context)


def event_view(request, event_id, event_code):
    '''This view leads to a single event landing page.'''
    event = Event.objects.get(pk=event_id, code=event_code)

    event_templates = Template.objects.select_related('owner').prefetch_related(
        'custom_fields').filter(event_id=29, event__code=event_code)
    # print([template.custom_fields.all() for template in event_templates])

    image = ''
    organizer_image = event_templates.first()
    if organizer_image:
        image = organizer_image.owner.images.all().first()

    context = {'page': 'Event', 'event': event,
               'event_templates': event_templates, 'organizer_image': image}
    return render(request, 'frontend_demo/order-of-service.html', context)


def login(request):
    '''user sign up to get authenticated.'''

    context = {'page':'login'}

    return render(request,'frontend_demo/login.html',context)