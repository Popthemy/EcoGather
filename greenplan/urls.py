from django.urls import path
from greenplan.views import EventApiView

urlpatterns = [
    path('events/', view=EventApiView.as_view(), name='all_event'),
]
