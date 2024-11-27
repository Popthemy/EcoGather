from django.urls import path,include
from greenplan import views,image_views as im_views,qr_code_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('organizers',viewset=views.OrganizerViewSet,basename='organizers')


""" Variable like `organizer_pk`, event_pk if changed can cause permission not to be functional.
    Check the permissions before changing """


urlpatterns = [

    path('organizers/<uuid:organizer_pk>/addresses/', view=views.AddressApiView.as_view(), name='addresses'),
    path('organizers/<uuid:organizer_pk>/addresses/<int:pk>/', view=views.AddressDetailApiView.as_view(), name='address-detail'),
    path('programs/',view=views.ProgramApiView.as_view(),name='programs'),
    path('programs/<int:pk>/',view=views.ProgramDetailApiView.as_view(),name='programs-detail'),

    path('events/', view=views.EventApiView.as_view(), name='events'),
    path('events/<int:pk>/',view=views.EventDetailApiView.as_view(),name='events-detail'),
    path('templates/',view=views.TemplateLibraryApiView.as_view(),name='templates'),
    path('events/<int:event_pk>/templates/',view=views.EventTemplateApiView.as_view(),name='event-templates'),
    path('events/<int:event_pk>/templates/<int:pk>/',view=views.EventTemplateDetailApiView.as_view(),name='event-templates-detail'),
    path('templates/<int:template_pk>/custom_fields/',view=views.CustomFieldApiView.as_view(),name='template_custom_fields'),
    path('templates/<int:template_pk>/custom_fields/<int:pk>/',view=views.CustomFieldDetailApiView.as_view(),name='template-custom_fields-detail'),

    #images
    path('organizers/images/', im_views.ListOrganizerImageApiView.as_view(), name='all-organizers-images'),
    path('organizers/<uuid:organizer_pk>/images/',im_views.OrganizerImageApiView.as_view(),name='organizer-images'),
    path('organizers/<uuid:organizer_pk>/images/<int:pk>/', im_views.OrganizerImageDetailApiView.as_view(),name='organizer-image-detail'),
    path('events/images/',im_views.ListEvenImageApiView.as_view(),name='all-events-images'),
    path('events/<int:event_pk>/images/',im_views.EventImageApiView.as_view(),name='event-images'),
    path('events/<int:event_pk>/images/<int:pk>/',im_views.EventImageDetailApiView.as_view(),name='event-image-detail'),

    path('generate_qr/',qr_code_views.generate_qr_code,name='generate_qr_code'),
    path('',include(router.urls)),

]
