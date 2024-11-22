from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from rest_framework import status
from model_bakery import baker
from greenplan.models import Program,Event
from django.shortcuts import get_object_or_404
import pytest
# Create your tests here.

User = get_user_model()


@pytest.fixture()
def queryset_url():
    '''Method available : Post and Get(return queryset) api/programs/'''
    return reverse_lazy('programs')


@pytest.mark.skip
@pytest.mark.django_db
class TestCreateListProgram:
    '''Applied permission is IsAdminOrReadOnly'''

    def test_if_user_is_anonymous_returns_401(self, api_client, queryset_url):
        # Arrange
        url = queryset_url

        # Act
        response = api_client.post(url, {'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, queryset_url, authenticate):
        # Arrange
        url = queryset_url

        # Act
        authenticate(is_staff=False)
        response = api_client.post(url, {'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_returns_201(self, api_client, queryset_url, authenticate):
        # Arrange
        url = queryset_url

        # Act
        authenticate(is_staff=True)
        response = api_client.post(url, {'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['title'] == 'a'
        assert 'id' in response.data['data']

    def test_if_admin_and_invalid_data_returns_400(self, api_client, queryset_url):
        # Arrange
        url = queryset_url

        # Act
        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post(url, {'title': ''})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'id' not in response.data

    def test_if_anonymous_returns_200(self, api_client, queryset_url):
        program1 = baker.make(Program)

        response = api_client.get(queryset_url)

        assert response.status_code == status.HTTP_200_OK
        assert program1.id == response.data['data'][0]['id']

    def test_if_admin_returns_200(self, api_client, queryset_url, authenticate):
        program1 = baker.make(Program)

        authenticate(is_staff=True)
        response = api_client.get(queryset_url)

        assert response.status_code == status.HTTP_200_OK
        assert program1.id == response.data['data'][0]['id']


@pytest.fixture()
def object_url():
    '''Method available : Post and Get(return queryset) api/programs/:id'''
    def url(program_id):
        return reverse_lazy('programs-detail', kwargs={'pk': program_id})
    return url


@pytest.mark.skip
@pytest.mark.django_db
class TestRetrieveProgram:
    '''Applied permission is IsAdminOrReadOnly'''

    # positive case
    @pytest.mark.parametrize(
        'user_type, expected_status_code', [
            ('anonymous', 200),
            ('authenticated_user', 200),
            ('admin', 200)
        ]
    )
    def test_for_all_user_types_and_valid_program_returns_200(self, api_client, object_url, authenticate, user_type, expected_status_code):
        '''This represent three test using the parametrize function of pytest.
        A single test takes multiple argument help us to test for all user types at once.'''
        
        program = baker.make(Program)
        id = program.id

        if user_type == 'authenticated_user':
            authenticate(is_staff=False)

        if user_type == 'admin':
            authenticate(is_staff=True)

        response = api_client.get(object_url(id))

        assert response.status_code == expected_status_code
        assert program.id == response.data['id']

    # negative case
    @pytest.mark.parametrize(
        'user_type, expected_status_code', [
            ('anonymous', 404),
            ('authenticated_user', 404),
            ('admin', 404)
        ]
    )
    def test_for_all_user_types_and_invalid_program_returns_404(self, api_client, object_url, authenticate, user_type, expected_status_code):
        '''This represent three test using the parametrize function of pytest.
        A single test takes multiple argument help us to test for all user types at once.'''
        
        program = baker.make(Program)
        id = program.id + 1

        if user_type == 'authenticated_user':
            authenticate(is_staff=False)

        if user_type == 'admin':
            authenticate(is_staff=True)

        response = api_client.get(object_url(id))
        assert response.status_code == expected_status_code


@pytest.mark.skip
@pytest.mark.django_db
class TestUpdateProgram:
    @pytest.mark.skip
    @pytest.mark.parametrize('user_type,expected_response',
                             [('anonymous',401),('authenticated_user',403)])
    def test_if_user_and_anonymous(self,api_client,object_url,authenticate,user_type,expected_response):
        program = baker.make(Program)
        url = object_url(program.id)

        if user_type == 'authenticated_user':
            #force authenticate the user
            authenticate(is_staff=False)

        response = api_client.patch(url,{"featured_event_id": 1})

        assert response.status_code == expected_response


    def test_patch_if_user_is_admin_and_valid_program_returns_200(self,api_client,authenticate,object_url,program):

        url = object_url(program.id)
        print(f'Retrieved object: {get_object_or_404(Program,pk=program.id)}')

        authenticate(is_staff=True)
        #{'title': 'new program title'}
        response = api_client.patch(url,{'title': 'new program title'})
        print(response.data)

        assert response.status_code == 200
        assert response.data['title'] ==  'new program title'

    def test_put_if_user_is_admin_and_valid_program_returns_200(self,api_client,authenticate,object_url,program):

        url = object_url(program.id)
        print(f'Retrieved object: {get_object_or_404(Program,pk=program.id)}')

        authenticate(is_staff=True)
        # {'title': 'new program title'}

        response = api_client.put(url, {'title': program.title})
        print(response.data)

        assert response.status_code == 200
        assert response.data['title'] ==  program.title




