'''Include views for creating user and profile on the demo frontend'''
from .forms import CreateUserForm,OrganizerForm
from myuser.models import CustomUser
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model,login
from greenplan.models import Organizer
from django.urls import reverse

User = get_user_model()


def create_user(request):
    '''Create a new user and redirect to a form to edit your organizer profile'''

    if request.user.is_authenticated:
        # in case a user is authenticated already
        message = f'Welcome {request.user.organizer.username} 😃'
        messages.info(request,message)
        return redirect('/')
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
            return redirect(request.GET.get('next',reverse('edit_organizer_profile',kwargs={'user_id': user.id})))

    context = {'page':'Register Page','form':form}
    return render(request,'frontend_demo/login-register.html',context)


def create_or_update_organizer(request,user_id):

    organizer , _= Organizer.objects.get_or_create(user=request.user)
    form = OrganizerForm(instance=organizer)

    if request.method == 'POST':
        form = OrganizerForm(request.POST, instance=organizer)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Organizer details updated successfully!')
            return redirect(request.GET.get('next','events'))
        
    context = {'page':'Organizer edit','form': form}
    return render(request, 'frontend_demo/create-or-update-organizer.html', context)


