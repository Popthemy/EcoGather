from django.urls import path
from greenplan.views import EventView

urlpatterns = [
    path('events/', view=EventView.as_view(), name='all_event'),
]
