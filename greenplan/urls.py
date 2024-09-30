from django.urls import path
from greenplan.views import EventApiView,list_events

urlpatterns = [
    path('events/', view=EventApiView.as_view(), name='all_event'),
    path('event_list/',list_events,name='func_event')
]
