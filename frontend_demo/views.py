from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login
from django.contrib import messages
from greenplan.models import Event, Template,Program

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
        events = Event.objects.prefetch_related('images').filter(program__title=filter_by_program_title)
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
                return redirect('events')
            else:
                message = 'Invalid Password!'
                messages.error(request,message)
                return redirect(request.get_full_path())
        
        message = 'Invalid Email'
        messages.error(request,message)

    context = {'page':'login'}

    return render(request,'frontend_demo/login.html',context)


def templates_view(request):
    '''this view provides list of all templates, we can click to clone a templates for our event'''

    templates = Template.objects.all()

    context = {'page':'templates','templates':templates}

    return render(request,'frontend_demo/bulletins.html',context)


def clone_template(request,template_id,template_code):

    templates = Template.objects.all()

