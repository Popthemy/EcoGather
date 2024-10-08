from django.urls import path,include
from greenplan import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('organizers',viewset=views.OrganizerViewSet,basename='organizers')


urlpatterns = [
    path('',include(router.urls)),
    path('events/', view=views.EventApiView.as_view(), name='events'),
    # path('organizers/', view=views.OrganizerApiView.as_view(), name='organizers'),
    # path('organizer_details/<uuid:pk>/', view=views.OrganizerDetailApiView.as_view(), name='organizer_details'),
    path('organizers/<uuid:pk>/addresses/', view=views.AddressApiView.as_view(), name='addresses'),
    path('organizers_addresses/<int:pk>/', view=views.AddressDetailApiView.as_view(), name='address_details'),
]
