from django.urls import path
from greenplan.views import EventApiView,list_events,organizer_detail

urlpatterns = [
    path('events/', view=EventApiView.as_view(), name='all_event'),
    # sample
    path('event_list/',list_events,name='func_event'),
    path('organizer/<uuid:pk>/',organizer_detail,name='organizer_detail')
]
