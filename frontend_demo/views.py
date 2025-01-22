from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from greenplan.models import Event, Template, Program, Organizer, EventComment
from django.core.exceptions import ValidationError
from greenplan.utils import track_impression
from django.utils import timezone
from .forms import CommentForm

# Create your views here.

""" Include page in every view context data so we can track the page you are currently working on from the title of the HTML page.
e.g {"page":"Event"}
"""

User = get_user_model()


def index(request):
    '''
    Include the events and the program we have. 
    Used featured event image as the program image  '''

    filter_by_program_title = request.GET.get('program', None)

    if filter_by_program_title:
        events = Event.base_manager.select_related('program').prefetch_related(
            'images').filter(program__title__icontains=filter_by_program_title)
    else:
        events = Event.base_manager.select_related(
            'program').prefetch_related('images').all()

    programs = Program.objects.select_related(
        'featured_event').prefetch_related('featured_event__images').all()

    username = request.user.organizer.username if request.user.is_authenticated else None
    context = {'page': 'Home page', 'current_user':  username,
               'events': events, 'programs': programs}
    return render(request, 'frontend_demo/events.html', context)


def event_detail(request, event_id, event_code):
    '''This view leads to a single event landing page.'''
    event = Event.objects.get(pk=event_id, code=event_code)

    # for tracking impression
    track_impression(request, event)

    # current path for redirect after successful comment
    current_url = request.get_full_path()

    event_templates = Template.objects.select_related('owner').prefetch_related(
        'custom_fields').filter(event=event)

    # reading event comments
    comments = EventComment.objects.filter(event=event)

    # including image
    image = ''
    organizer_image = event_templates.first()
    if organizer_image:
        image = organizer_image.owner.images.all().first()

    # creating and editing comment

    comment_id = request.GET.get('comment_id', None)
    comment_to_edit = None
    if comment_id:
        comment_to_edit = EventComment.objects.get(
            id=comment_id, event_id=event.id)
        comment_form = CommentForm(
            initial={'content': comment_to_edit.content})
    else:
        comment_form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content'].strip()

            # edit comment
            if comment_id and comment_to_edit:
                comment_to_edit.content = content
                comment_to_edit.save()
                message = 'Comment Updated!'
                messages.success(request, message)
                return redirect('event_detail', event_id=event_id, event_code=event_code)

            # create comment
            if request.user.is_authenticated and len(content):
                EventComment.objects.create(
                    event_id=event_id, user_id=request.user.id, content=content)
                message = 'Commenting Successful'
                messages.success(request, message)
                return redirect(current_url)

        else:
            message = 'Commenting Unsuccessful'
            messages.success(request, message)
            return redirect(current_url)

    context = {'page': 'Event', 
               'current_user': request.user.organizer.username if request.user.is_authenticated else None, 
               'event': event,
               'event_templates': event_templates,
                'organizer_image': image, 
                'comments': comments,
               'current_time': timezone.now(), 
               'comment_form': comment_form, 
               'edit_comment': comment_to_edit
               }

    return render(request, 'frontend_demo/order-of-service.html', context)


def delete_event_comment(request, event_id, comment_id):
    '''After deleting comment it should reload the current page'''

    comment = EventComment.objects.get(id=comment_id, event_id=event_id)
    message = 'No permission to delete someone else message'

    if request.user == comment.user:
        comment.delete()
        message = 'Comment Deleted'
    messages.success(request, message)
    return redirect(request.GET.get('next', 'events'))


def login_view(request):
    '''user sign up to get authenticated.'''
    if request.user.is_authenticated:
        # in case a user is authenticated already
        message = f'Welcome {request.user.organizer.username} 😃'
        messages.info(request,message)
        return redirect('/')
        

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()
        if user:
            sign_in_user = authenticate(
                request, email=email, password=password)
            if sign_in_user:
                login(request, sign_in_user)
                message = 'Login Successful!'
                messages.success(request, message)
                return redirect(request.GET.get('next') if 'next' in request.GET else 'events')
            else:
                message = 'Invalid Password!'
                messages.error(request, message)
                return redirect(request.get_full_path())

        message = 'Invalid Email'
        messages.error(request, message)

    context = {'page': 'login'}

    return render(request, 'frontend_demo/login-register.html', context)


def templates_view(request):
    '''This view provides list of all templates, we can click to clone a templates for our event'''

    templates = Template.objects.all()
    message = 'Select one of the template to clone. A Template to be clone must have more than one field'
    messages.info(request, message)

    username = request.user.organizer.username if request.user.is_authenticated else None
    context = {'page': 'Templates',
               'current_user': username, 'templates': templates}
    return render(request, 'frontend_demo/bulletins.html', context)


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
                template.clone_template(
                    user_id=current_user_id, event_id=event_id)
            except ValidationError as e:
                messages.error(request, message=str(e))
                return redirect(request.get_full_path())

            # Redirect to event details page with event_id and event_code as parameters
            return redirect('event_detail', event_id=event_id, event_code=event_code)

        # Handle missing input
        message = 'Please select an event to link with the cloned template.'
        messages.error(request, message)
        return redirect(request.get_full_path())

    events = Event.objects.filter(organizer_id=current_user_id)

    username = request.user.organizer.username if request.user.is_authenticated else None
    context = {'page': 'Clone Template',
               'current_user': username, 'events': events}
    return render(request, 'frontend_demo/clone_event_template.html', context)


def logout_view(request):
    message = 'Logout Successful. See you around..'
    messages.success(request, message)
    logout(request)
    return redirect('events')


def organizer_detail(request, organizer_id):
    organizer = Organizer.objects.get(user_id=organizer_id)

    image = ''
    organizer_image = organizer.images.all()
    if organizer_image:
        image = organizer_image.first()

    username = request.user.organizer.username if request.user.is_authenticated else None
    context = {'page': f'{ organizer.username if organizer else Organizer }',
               'current_user': username, 'organizer': organizer, 'organizer_image': image}

    return render(request, 'frontend_demo/organizer_detail.html', context)

