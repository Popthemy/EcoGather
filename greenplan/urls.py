from django.urls import path,include
from greenplan import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('organizers',viewset=views.OrganizerViewSet,basename='organizers')




urlpatterns = [
    path('',include(router.urls)),
    path('organizers/<uuid:organizer_pk>/addresses/', view=views.AddressApiView.as_view(), name='addresses'),
    path('organizers/<uuid:organizer_pk>/addresses/<int:pk>/', view=views.AddressDetailApiView.as_view(), name='address_details'),
    path('programs/',view=views.ProgramApiView.as_view(),name='programs'),

    path('events/', view=views.EventApiView.as_view(), name='events'),
    # path('organizers/', view=views.OrganizerApiView.as_view(), name='organizers'),
    # path('organizer_details/<uuid:pk>/', view=views.OrganizerDetailApiView.as_view(), name='organizer_details'),
]
