'''Include views for creating user and profile on the demo frontend'''
from .forms import CreateUserForm
from myuser.models import CustomUser
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model,authenticate,login


User = get_user_model()


def create_user(request):
    '''Create a new user and redirect to a form to edit your organizer profile'''
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # register user
            user = User.objects.create_user(email=email)
            user.set_password(password)
            user.save()

            # login user
            login(request,user)

            # redirect to homepage
            messages.success(request,'Account successfully created')
            return redirect(request.GET.get('next','events'))

    context = {'page':'Register Page','form':form}
    return render(request,'frontend_demo/login-register.html',context)



