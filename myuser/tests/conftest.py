from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from greenplan.models import Organizer, Address, OrganizerImage
from model_bakery import baker
import pytest

# define fixture that are global

User = get_user_model()


@pytest.fixture
def api_client():
    '''a fixture that will be imported without us needing to explicitly do it'''
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        '''for authenticating user to become admin or ordinary user'''
        User = get_user_model()
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate


@pytest.fixture
def user():
    return User.objects.create_user(email='testuser@email.com', password='testPassword')


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

