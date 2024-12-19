from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from greenplan.models import Event, Template,Program
from django.core.exceptions import ValidationError

# Create your views here.

""" Include page in every view context data so we can track the page you are currently working on from the title of the HTML page.
e.g {"page":"Event"}
"""

User = get_user_model()


def index(request):
    '''
    Include the events and the program we have. 
    Used featured event image as the program image  '''

    filter_by_program_title = request.GET.get('program',None)

    if filter_by_program_title:
        events = Event.objects.prefetch_related('images').filter(program__title__icontains=filter_by_program_title)
    else:
        events = Event.objects.prefetch_related('images').all()

    programs = Program.objects.select_related('featured_event').prefetch_related('featured_event__images').all()

    context = {'page': 'Home page', 'events': events,'programs':programs}
    return render(request, 'frontend_demo/events.html', context)


def event_view(request, event_id, event_code):
    '''This view leads to a single event landing page.'''
    event = Event.objects.get(pk=event_id, code=event_code)

    event_templates = Template.objects.select_related('owner').prefetch_related(
        'custom_fields').filter(event_id=event_id, event__code=event_code)
    # print([template.custom_fields.all() for template in event_templates])

    image = ''
    organizer_image = event_templates.first()
    if organizer_image:
        image = organizer_image.owner.images.all().first()

    context = {'page': 'Event', 'event': event,
               'event_templates': event_templates, 'organizer_image': image}
    return render(request, 'frontend_demo/order-of-service.html', context)


def login_view(request):
    '''user sign up to get authenticated.'''

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()
        if user:
            sign_in_user = authenticate(request,email=email,password=password)
            if sign_in_user:
                login(request,sign_in_user)
                message = 'Login Successful!'
                messages.success(request,message)
                return redirect( request.GET.get('next') if 'next' in request.GET else 'events')
            else:
                message = 'Invalid Password!'
                messages.error(request,message)
                return redirect(request.get_full_path())

        message = 'Invalid Email'
        messages.error(request,message)

    context = {'page':'login'}

    return render(request,'frontend_demo/login.html',context)


def templates_view(request):
    '''This view provides list of all templates, we can click to clone a templates for our event'''

    templates = Template.objects.all()
    message = 'Select one of the template to clone.A Template to be clone must have more than one field'
    messages.info(request, message)

    context = {'page':'Templates','templates':templates}
    return render(request,'frontend_demo/bulletins.html',context)


@login_required(login_url='login')
def clone_template_view(request, template_id, template_code):
    '''For cloning a template, user needs to select an event to link it to'''
    template = Template.objects.get(pk=template_id, code=template_code)
    current_user_id = request.user.id

    if request.method == "POST":
        # Retrieve event_id and event_code from POST data
        event_id = request.POST.get('event_id')  # Match form 'name' attribute
        event_code = request.POST.get('event_code')  # Sent via hidden input

        if event_id and event_code:
            # Call the clone method and pass the required parameters
            try:
                template.clone_template(user_id=current_user_id, event_id=event_id)
            except ValidationError as e:
                messages.error(request,message=str(e))
                return redirect(request.get_full_path())
            
            # Redirect to event details page with event_id and event_code as parameters
            return redirect('event_detail', event_id=event_id, event_code=event_code)

        # Handle missing input
        message = 'Please select an event to link with the cloned template.'
        messages.error(request, message)
        return redirect(request.get_full_path())

    events = Event.objects.filter(organizer_id=current_user_id)

    context = {'page': 'Clone Template', 'events': events}
    return render(request, 'frontend_demo/clone_event_template.html', context)


def logout_view(request):
    message = 'Logout Successful. See you around..'
    messages.success(request,message)
    logout(request)
    return redirect('events')
    
