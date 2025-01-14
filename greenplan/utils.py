'''
Keep code that doesn't aren't views function/class here'''
from greenplan.models import EventImpression, Event
from django.db.models import Q


def track_impression(request, event: Event):
    '''
    Track unique impressions and update our impression on the event object.
    Uniqueness is based on some attributes as Event ,Sessions key, User(anonymous and authenticated)..
    '''

    session_key = request.session.session_key
    user = request.user if request.user.is_authenticated else None
    ip_address = request.client_ip

    try:
        _ , created = EventImpression.objects.get_or_create(
            event=event,
            user=user,
            ip_address=ip_address,
            session_key=session_key
        )

        if created:
            event.impressions += 1
            event.save()

    except Exception:
        pass
