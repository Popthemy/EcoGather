from django.urls import path
from greenplan import views

urlpatterns = [
    path('events/', view=views.EventApiView.as_view(), name='all_event'),
    path('organizers/', view=views.OrganizerListApiView.as_view(), name='organizer_detail'),
    path('organizer_details/<uuid:pk>/', view=views.OrganizerDetailApiView.as_view(), name='organizer_details'),
]
