from django.urls import path
from . import views

urlpatterns = [
  path('data',views.import_dummy_data,name='data'),
  path('demo_event/',views.list_event,name='list_event')
    
]
