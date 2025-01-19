from django.urls import path
from . import views,demo_user_views


urlpatterns = [
  
    path('',views.index,name='events'),
    path('events/<int:event_id>/<str:event_code>/',views.event_detail,name='event_detail'),
    path('templates/',views.templates_view,name='templates'),
    path('templates/<int:template_id>/<str:template_code>/',views.clone_template_view,name='clone_template'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('events/<int:event_id>/comments/<int:comment_id>/delete/',views.delete_event_comment,name='event_comment_delete'),
    path('organizers/<uuid:organizer_id>/',views.organizer_detail,name='organizer_detail'),

    # user
    path('users/register/',demo_user_views.create_user,name='register_user'),

]
