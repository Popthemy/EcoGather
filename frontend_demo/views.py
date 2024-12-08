from django.shortcuts import render
from greenplan.models import Event,Template
# Create your views here.


def demo_view(request):
    event = Event.objects.get(pk=29)

    event_templates = Template.objects.select_related('owner').prefetch_related('custom_fields').filter(event_id=29)
    # print([template.custom_fields.all() for template in event_templates])

    organizer_images = event_templates.first().owner.images.all()

    context = {'page': 'Event', 'event': event, 'event_templates':event_templates,'organizer_image':organizer_images.first()}
    return render(request, 'frontend_demo/order-of-service.html', context)
