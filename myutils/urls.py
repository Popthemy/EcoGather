from django.urls import path
from .views import import_dummy_data

urlpatterns = [
  path('data',view=import_dummy_data,name='data')
    
]
