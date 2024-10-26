from django.urls import path,include
from greenplan import views,image_views as im_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('organizers',viewset=views.OrganizerViewSet,basename='organizers')




urlpatterns = [
    path('organizers/<uuid:organizer_pk>/addresses/', view=views.AddressApiView.as_view(), name='addresses'),
    path('organizers/<uuid:organizer_pk>/addresses/<int:pk>/', view=views.AddressDetailApiView.as_view(), name='address_detail'),
    path('programs/',view=views.ProgramApiView.as_view(),name='programs'),
    path('programs/<int:pk>/',view=views.ProgramDetailApiView.as_view(),name='programs-detail'),

    path('events/', view=views.EventApiView.as_view(), name='events'),
    path('events/<int:pk>/',view=views.EventDetailApiView.as_view(),name='events-detail'),
    path('templates/',view=views.TemplateLibraryApiView.as_view(),name='templates'),
    path('events/<int:event_pk>/templates/',view=views.EventTemplateApiView.as_view(),name='event_templates'),
    path('events/<int:event_pk>/templates/<int:pk>/',view=views.EventTemplateDetailApiView.as_view(),name='event_templates_detail'),
    path('templates/<int:template_pk>/custom_fields/',view=views.CustomFieldApiView.as_view(),name='template_custom_fields'),
    path('templates/<int:template_pk>/custom_fields/<int:pk>/',view=views.CustomFieldDetailApiView.as_view(),name='template_custom_fields_detail'),

    #images
    path('organizers/images/', im_views.ListOrganizerImageApiView.as_view(), name='all_organizers_images'),
    path('organizers/<uuid:organizer_pk>/images/',im_views.OrganizerImageApiView.as_view(),name='organizer_images'),
    path('organizers/<uuid:organizer_pk>/images/<int:pk>/', im_views.OrganizerImageDetailApiView.as_view(),name='organizer_image_details'),
    path('events/images/',im_views.ListEvenImageApiView.as_view(),name='all_events_images'),
    
    path('',include(router.urls)),


]
