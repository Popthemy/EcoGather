'''Include views for creating user and profile on the demo frontend'''
from .forms import CreateUserForm
from myuser.models import CustomUser
from django.shortcuts import HttpResponse


def create_user(request):
    form = CreateUserForm()

    if request.method == 'POST':
        print(request.POST)

  
    return HttpResponse(form)
