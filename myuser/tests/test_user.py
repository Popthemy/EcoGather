from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from rest_framework import status
from model_bakery import baker
from myutils.reusable_func import get_jwt_tokens
import pytest

User = get_user_model()


@pytest.mark.skip
@pytest.mark.django_db
class TestCreateUser:

    # positive case
    def test_if_anonymous_and_valid_data_returns_201(self, api_client):

        url = reverse_lazy('register_user')

        test_data = {
            'email': 'testuser@email.com',
            'password': 'testPassword',
            'confirm_password': 'testPassword'
        }

        response = api_client.post(url, test_data)

        assert response.status_code == 201
        assert 'token' in response.data
        assert 'id' in response.data['data']

    @pytest.mark.parametrize('user_type,expected_response',
                             [('admin', 403), ('authenticated_user', 403)])
    def test_if_admin_or_authenticated_returns_403(self, api_client, authenticate, user_type, expected_response):
        '''This includes two test: for authenticated user, admin'''
        url = reverse_lazy('register_user')

        test_data = {
            'email': 'testuser@email.com',
            'password': 'testPassword',
            'confirm_password': 'testPassword'
        }

        authenticate(is_staff=False)
        if user_type == 'admin':
            authenticate(is_staff=True)

        response = api_client.post(url, test_data)

        assert response.status_code == expected_response
        assert 'token' not in response.data

    # negative case
    @pytest.mark.parametrize('missing_data',
                             [('email'), ('password'), ('confirm_password')])
    def test_if_anonymous_and_missing_data_returns_400(self, api_client, missing_data):
        ''''test for invlaid cases of test such as scenarios where required field are empty'''
        url = reverse_lazy('register_user')

        test_data = {
            'email': 'testuser@email.com',
            'password': 'testPassword',
            'confirm_password': 'testPassword'
        }

        if missing_data in ['email', 'password', 'confirm_password']:
            test_data[missing_data] = ''

        response = api_client.post(url, test_data)

        assert response.status_code == 400
        assert missing_data in response.data
        assert 'token' not in response.data


@pytest.mark.skip
@pytest.mark.django_db
class TestLoginUser:

    # postive case
    def test_if_anonymous_and_valid_user_returns_200(self, api_client):
        user = User.objects.create_user(
            email='testuser@email.com', password='testPassword')

        url = reverse_lazy('login_user')

        test_data = {'email': 'testuser@email.com', 'password': 'testPassword'}

        response = api_client.post(url, test_data)

        assert response.status_code == 200
        assert 'token' in response.data
        assert response.data['data']['id'] == str(user.id)

    @pytest.mark.parametrize('user_type',
                             [('admin'),
                              ('authenticated_user')])
    def test_if_authenticated_user_or_admin_returns_403(self, api_client, user, user_type, authenticate):
        '''Already authenticated user has no permissions, meaning they aren't allowed to login again'''

        url = reverse_lazy('login_user')

        test_data = {'email': 'testuser@email.com', 'password': 'testPassword'}

        authenticate(is_staff=False)
        if user_type == 'admin':
            authenticate(is_staff=True)

        response = api_client.post(url, test_data)
        print(response.data)

        assert response.status_code == 403
        assert str(user.id) not in response.data

    # negative cases
    @pytest.mark.parametrize('incorrect_data',
                             [('email'),
                              ('password')])
    def test_if_anonymous_and_incorrect_details_returns_401(self, api_client, user, incorrect_data):
        url = reverse_lazy('login_user')
        test_data = {'email': 'testuser@email.com', 'password': 'testPassword'}

        if incorrect_data in ['email', 'password']:
            test_data[incorrect_data] = '123' + test_data[incorrect_data]

        response = api_client.post(url, test_data)

        assert response.status_code == 401

    @pytest.mark.parametrize('missing_data',
                             [('email'),
                              ('password')])
    def test_if_anonymous_and_missing_data_returns_401(self, api_client, user, missing_data):

        url = reverse_lazy('login_user')

        test_data = {'email': 'testuser@email.com', 'password': 'testPassword'}

        if missing_data in ['email', 'password']:
            test_data[missing_data] = ''

        response = api_client.post(url, test_data)

        assert response.status_code == 401
        assert missing_data in response.data['data']

@pytest.mark.skip
@pytest.mark.django_db
class TestRefreshToken:
    #positive cases
    def test_if_valid_token_returns_200(self,api_client,user):

        token = get_jwt_tokens(user)
        refresh_token = token['refresh']

        # test that our refresh token is valid by using it to get the new  token
        assert len(refresh_token) == 279

        response = api_client.post(reverse_lazy('token_refresh'),{'refresh': refresh_token})
        print(f'data refresh endpoint :{response.data}')

        assert response.status_code == 200
        assert 'access' in response.data

    def test_if_invalid_token_returns_401(self,api_client,user):

        token = get_jwt_tokens(user)
        refresh_token = token['refresh']
        refresh_token = refresh_token +'abc'

        # test that our refresh token is valid by using it to get the new  token
        response = api_client.post(reverse_lazy('token_refresh'),{'refresh': refresh_token})
        print(f'data refresh endpoint :{response.data}')

        assert response.status_code == 401



@pytest.mark.skip
@pytest.mark.django_db
class TestLogoutUser:
    '''Permission class = IsAuthenticated'''

    #positive cases
    @pytest.mark.parametrize('user_type',['admin','authenticated_user'])
    def test_if_user_is_authenticated_or_admin_and_valid_token_returns_200(self,api_client,user,authenticate,user_type):
        url = reverse_lazy('logout_user') #logout with refresh token

        token = get_jwt_tokens(user)
        refresh_token = token['refresh']

        authenticate(is_staff=False)
        if user_type == 'admin':
            authenticate(is_staff=True)
            print(user.is_staff)

        response = api_client.post(url,{'refresh': refresh_token})
        print(response.data)

        assert response.status_code == 200

    # @pytest.mark.skip
    def test_if_user_anonymous_returns_401(self,api_client):
        # anonymous users has no token and aren't allowed at this endpoint because they have no token.
        url = reverse_lazy('logout_user')

        response = api_client.post(url,{'refresh':'ap45-y5-6'*28})

        assert response.status_code == 401


    #negative cases
    @pytest.mark.parametrize('user_type',['admin','authenticated_user'])
    def test_if_user_is_authenticated_or_admin_and_invalid_token_returns_400(self,api_client,user,authenticate,user_type):
        url = reverse_lazy('logout_user') # unable to logout with invalid refresh token

        refresh_token = 'invalid_token'

        authenticate(is_staff=False)
        if user_type == 'admin':
            authenticate(is_staff=True)

        response = api_client.post(url,{'refresh': refresh_token})
        print(response.data)

        assert response.status_code == 400

    def test_expired_token_returns_400(self,api_client,user,authenticate):
        url = reverse_lazy('logout_user') # unable to logout with expired refresh token

        token = get_jwt_tokens(user)
        refresh_token = token['refresh']

        authenticate(is_staff=False)
        
        first_response = api_client.post(url,{'refresh': refresh_token})
        assert first_response.status_code == 200

        second_response = api_client.post(url,{'refresh': refresh_token})
        print(second_response.data)
        assert second_response.status_code == 400
