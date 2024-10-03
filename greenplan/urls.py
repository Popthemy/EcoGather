from django.urls import path
from greenplan import views

urlpatterns = [
    path('events/', view=views.EventApiView.as_view(), name='events'),
    path('organizers/', view=views.OrganizerApiView.as_view(), name='organizers'),
    path('organizer_details/<uuid:pk>/', view=views.OrganizerDetailApiView.as_view(), name='organizer_details'),
    path('organizer_details/<uuid:pk>/addresses/', view=views.AddressApiView.as_view(), name='addresses'),
    path('addresses/<int:pk>/', view=views.AddressDetailApiView.as_view(), name='address_details'),
]
