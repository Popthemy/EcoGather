from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from greenplan.models import Organizer, Event, Program, Template, CustomField, Address, OrganizerImage, EventImage
from model_bakery import baker
from myutils.reusable_func import get_jwt_tokens
import pytest


# define fixture that are global

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    '''a fixture that will be imported without us needing to explicitly do it'''
    return APIClient()


@pytest.fixture
def user(api_client, user_tokens):
    '''When a new user is created an Organizer is create by default, 
    this should also retrieve user token and attach access token to the header'''

    def token_needed(add_token=False):
        user = User.objects.create_user(
        email='testuser@email.com', password='testPassword')

        # Retrieve access token
        if add_token:
            print(f'token needed in the user and has been generated')
            access_token, _ = user_tokens(user)

            # attach access_token to the header of th request
            api_client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')
        return user
    return token_needed

@pytest.fixture
def admin_user(api_client, user_tokens):
    '''create a superuser and also attach token to the header'''

    def token_needed(add_token=False):
        super_user = User.objects.create_superuser(
        email='other@example.com', password='password4test')

        # Retrieve access token
        if add_token:
            print(f'token needed in the super user and has been generated')
            access_token, _ = user_tokens(super_user)

            # attach access_token to the header of th request
            api_client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')
        return super_user
    return token_needed


@pytest.fixture
def user_tokens():
    '''get the access and refresh tokens for user (access,refresh)'''
    def get_user_tokens(user: User) -> tuple:
        token = get_jwt_tokens(user)
        return token['access'], token['refresh']
    return get_user_tokens


@pytest.fixture
def authenticate(api_client, user):
    def do_authenticate(is_staff=False):
        '''Role:
        1> Includes access token in the header
        2> Making users to become admin or ordinary user

        Returns:
          authenticated user as user or admin and the user(so as to reduce our parameters)'''

        # Generate the JWT token for the user
        token = get_jwt_tokens(user)
        access_token = token['access']

        # Add the token to the Authorization header
        api_client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate


@pytest.fixture
def organizer(user):
    """Fixture to create an organizer"""
    return baker.make(Organizer, user=user, username="organizer_1", email="organizer1@example.com", phone_number="1234567890")


@pytest.fixture
def organizer_image(organizer):
    """Fixture to create an organizer image"""
    return baker.make(
        OrganizerImage,
        organizer=organizer,
        image_url='organizer_image.png',
        priority=OrganizerImage.MEDIUM
    )


@pytest.fixture
def address(organizer):
    """Fixture to create an address for the organizer"""
    return baker.make(
        Address,
        organizer=organizer,
        street_number=123,
        street_name="Main Street",
        city="Ogbomoso",
        state="Oyo",
        zip_code=210001,
        country="Nigeria"
    )


@pytest.fixture
def program():
    """Fixture to create a program"""
    return baker.make(Program, title="Conference")


@pytest.fixture
def event(organizer, program):
    """Fixture to create an event associated with organizer and program"""
    return baker.make(
        Event,
        code="EVENT2024",
        title="Annual Conference",
        description="A major annual conference",
        venue="Great Hall, Lautech",
        city="Ogbomoso",
        start_datetime=timezone.now(),
        end_datetime=timezone.now() + timezone.timedelta(hours=3),
        organizer=organizer,
        program=program
    )


@pytest.fixture
def event_image(event):
    """Fixture to create an event image"""
    return baker.make(
        EventImage,
        event=event,
        image_url='event_image.png',
        priority=EventImage.MEDIUM
    )


@pytest.fixture
def template(organizer, event):
    """Fixture to create a template, optionally linking to an event"""
    return baker.make(
        Template,
        owner=organizer,
        code="TEMPLATE001",
        title="Standard Template",
        event=event
    )


@pytest.fixture
def custom_field(template):
    """Fixture to create a custom field linked to the template"""
    return baker.make(
        CustomField,
        template=template,
        label="Processional Hymn EBH 20",
        content="Song Lead by the Choir",
        start_time="07:30",
        end_time="07:50"
    )
