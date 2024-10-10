from django.urls import path,include
from greenplan import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('organizers',viewset=views.OrganizerViewSet,basename='organizers')




urlpatterns = [
    path('',include(router.urls)),
    path('organizers/<uuid:organizer_pk>/addresses/', view=views.AddressApiView.as_view(), name='addresses'),
    path('organizers/<uuid:organizer_pk>/addresses/<int:pk>/', view=views.AddressDetailApiView.as_view(), name='address-detail'),
    path('programs/',view=views.ProgramApiView.as_view(),name='programs'),
    path('programs/<int:pk>/',view=views.ProgramDetailApiView.as_view(),name='programs-detail'),

    path('events/', view=views.EventApiView.as_view(), name='events'),
]
