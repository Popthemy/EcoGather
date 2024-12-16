from django.urls import path
from . import views


urlpatterns = [
  
    path('',views.index,name='events'),
    path('events/<int:event_id>/<str:event_code>/',views.event_view,name='event_detail'),
    path('login/',views.login,name='login_page'),
]
