from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from greenplan.models import Organizer
import pytest


User = get_user_model()


@pytest.mark.skip
@pytest.mark.django_db
class TestCreateOrganizer:
    '''When a user is created and Organizer is created also.There is one-one relationship between them'''

    def test_if_new_user_creates_organizer_returns_201(self, api_client, user):
        
        user = user(add_token=False)
        organizer = Organizer.objects.filter(
            pk=user.id).values('user', 'email')[0]

        assert organizer is not None
        assert organizer['email'] == user.email


@pytest.mark.skip
@pytest.mark.django_db
class TestRetrieveOrganizer:

    # positive cases
    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_get_organizer_list_returns_200(self, api_client, user, admin_user, user_type):
        """ Test retrieving a list of organizers. Admin sees all, regular user sees only their own."""
        #----------- Arrange
        # GET request to list organizers
        url = reverse_lazy('organizers-list')

        # Retrieve user and access token
        user = user(add_token=True)

        current_user = user
        if user_type == 'admin':
            current_user = admin_user(add_token=True)

        # ----------- Action 
        response = api_client.get(url)

        #-------- Assert
        assert response.status_code == 200

        if user_type == 'admin':
            assert len(response.data) == 2  # Admin sees both organizers

        if user_type == 'authenticated_user':
            # Regular user only sees themselves, this also test that they don't get to see list of organizers
            assert len(response.data) == 1
            assert response.data[0]['email'] == user.email

    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_get_organizer_by_id_returns_200(self, api_client, user, admin_user, user_type):
        """ Test retrieving an organizer by ID. A user can only see their own organizer profile while admin can see for all. """

        # Retrieve user and access token
        user = user(add_token=True)

        current_user = user
        if user_type == 'admin':
            current_user = admin_user(add_token=True)
        
        # GET request to retrieve non admin user
        url = reverse_lazy('organizers-detail', kwargs={'pk': user.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['email'] == user.email

    def test_if_admin_retrieve_someone_else_id_returns_200(self, api_client, user, admin_user):
        """ Test admin retrieving someone else id. Should return 2020."""

        # Retrieve user and access token
        user = user(add_token=False) # user created but we don't use their token
        admin = admin_user(add_token=True) # use the token of the

        # GET request to retrieve non admin user
        url = reverse_lazy('organizers-detail', kwargs={'pk': user.id})
        response = api_client.get(url)
        # print(response.data)

        assert response.status_code == 200
        assert response.data['id'] == str(user.id)

    def test_if_anonymous_returns_200(self, api_client):
        """ Test retrieving a list of organizers without authentication. Should return 401 Unauthorized."""
        
        # GET request to list organizers without authentication
        url = reverse_lazy('organizers-list')
        response = api_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 0
    
    # negative case
    @pytest.mark.parametrize('user_type', ['anonymous','admin', 'authenticated_user'])
    def test_get_invalid_id_returns_404(self, api_client, user, admin_user, user_type):
        """ Test retrieving a non-existent organizer. Should return 404. """

        invalid_id = '6c057454-8461-4d67-81d2-43a9e9865678'

        # Retrieve user and access
        current_user = '' #anonymouse user applied not token

        if user == 'user':
            current_user  = user(add_token=True)

        if user_type == 'admin':
            current_user = admin_user(add_token=True)

        # GET request to retrieve specific organizer
        url = reverse_lazy('organizers-detail', kwargs={'pk': invalid_id})
        response = api_client.get(url)
        print(response.data)

        # both user the user id which is not an admin,
        assert response.status_code == 404


@pytest.mark.skip
@pytest.mark.django_db
class TestUpdateOrganizer:
    #positive cases
    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_if_authenticated_user_or_admin_patch_returns_200(self, api_client, user, admin_user, user_type):
        """ Test PATCH method to update organizer data. Only the owner or admin should be able to update. """

        # Prepare the data
        update_data = {
            'username': 'updated_username',
            'first_name':'test',
        }

        # Retrieve user and access token
        user = user(add_token=True)

        current_user = user
        if user_type == 'admin':
            current_user = admin_user(add_token=True)

        # PUT request to update organizer's data
        url = reverse_lazy('organizers-detail', kwargs={'pk': user.id})
        response = api_client.patch(url, update_data)

        assert response.status_code == 200
        assert response.data['username'] == update_data['username']

    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_if_authenticated_user_or_admin_put_returns_200(self, api_client, user, admin_user, user_type):
        """ Test PUT method to update organizer data. Only the owner or admin should be able to update. """

        # Retrieve user and access token
        user = user(add_token=True)

        current_user = user
        if user_type == 'admin':
            current_user = admin_user(add_token=True)
    
        org_response = Organizer.objects.filter(pk=user.id).first() 
        assert org_response is not None

        # Prepare the data
        update_data = {
            'username': 'updated_username',
            'phone_number': 'org',
            'email': org_response.email
        }

        # PUT request to update organizer's data
        url = reverse_lazy('organizers-detail', kwargs={'pk': user.id})
        response = api_client.put(url, update_data)
        # print(f'before update: {org_response.__dict__}')
        # print(f'after update: {response.data}')

        assert response.status_code == 200
        assert response.data['email'] == update_data['email']
        assert response.data['username'] == update_data['username']

    #negative test
    def test_if_not_owner_put_return_403(self, api_client, user, admin_user):
        """ Test PUT method for a non-owner user. return 404 not found because a user can't see 
        someone else organizer profile. user try to update admin data"""

        # Prepare the data
        update_data = {
            'email': 'unauthorized_update@example.com'
        }

        # Retrieve user and access token
        user = user(add_token=True)
        admin = admin_user(add_token=False)

        # PUT request to update another user's organizer data
        url = reverse_lazy('organizers-detail', kwargs={'pk': admin.id})
        response = api_client.put(url, update_data)
        # print(f'updated organizer data: {response.data}')

        assert response.status_code == 403

    def test_if_not_owner_patch_return_403(self, api_client, user, admin_user):
        """ Test PUT method for a non-owner user. return 404 not found because a user can't see 
        someone else organizer profile. user try to update admin data"""

        # Prepare the data
        update_data = {
            'email': 'unauthorized_update@example.com'
        }

        # Retrieve user and access token
        user = user(add_token=True)
        admin = admin_user(add_token=False)

        # PUT request to update another user's organizer data
        url = reverse_lazy('organizers-detail', kwargs={'pk': admin.id})
        response = api_client.patch(url, update_data)
        # print(f'updated(patch) organizer data: {response.data}')

        assert response.status_code == 403

    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_if_invalid_data_authenticated_user_or_admin_put_returns_400(self, api_client, user, admin_user, user_type):
        """ Test PATCH method to update organizer data. Only the owner or admin should be able to update. """

        # Prepare the data
        update_data = {
            'username': 'updated_username',
        }

        # Retrieve user and access token
        user = user(add_token=True)

        current_user = user
        if user_type == 'admin':
            current_user = admin_user(add_token=True)

        # PUT request to update organizer's data
        url = reverse_lazy('organizers-detail', kwargs={'pk': user.id})
        response = api_client.put(url, update_data)

        assert response.status_code == 400
        assert update_data['username'] not in response.data

    def test_if_anonymous_put_returns_401(self, api_client,user):
        """ Test updating an organizers without authentication. Should return 401 Unauthorized."""
        
        # Prepare the data
        update_data = {
            'username': 'updated_username',
        }

        user = user(add_token=False)

        # No authentication for the user
        # PUT request to update organizer's data
        url = reverse_lazy('organizers-detail', kwargs={'pk': user.id})
        response = api_client.put(url, update_data)

        assert response.status_code == 401
        assert update_data['username'] not in response.data

    def test_if_anonymous_patch_returns_401(self, api_client,user):
        """ Test updating an organizers without authentication. Should return 401 Unauthorized."""
        
        # Prepare the data
        update_data = {
            'username': 'updated_username',
        }

        user = user(add_token=False)

        # No authentication for the user
        # PUT request to update organizer's data
        url = reverse_lazy('organizers-detail', kwargs={'pk': user.id})
        response = api_client.patch(url, update_data)

        assert response.status_code == 401
        assert update_data['username'] not in response.data


# @pytest.mark.skip
@pytest.mark.django_db
class TestDeleteOrganizer:
    '''
        Permission - IsAuthenticated
        Only the owner or admin should be able to delete.
    '''

    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_if_admin_or_authenticated_user_delete_return_204(self, api_client, user, admin_user,user_type):
        """ Test DELETE method to delete an organizer. Only the owner or admin should be able to delete. """

        # Retrieve user and access token
        user = user(add_token=True)

        current_user = user
        if user_type == 'admin':
            current_user = admin_user(add_token=True)
        
        id = current_user.id

        # DELETE request to remove the organizer
        url = reverse_lazy('organizers-detail', kwargs={'pk': id})
        response = api_client.delete(url)

        assert response.status_code == 204  # No content after successful deletion

        # after successful deletion of organizer the user should get deleted also
        assert not User.objects.filter(id=id).first()



    #negative cases
    @pytest.mark.parametrize('user_type,expected_response',[('authenticated_user',403),('anonymous',401)])
    def test_if_authenticated_user_delete_another_organizer_returns(self, api_client, user, admin_user,user_type,expected_response):
        """ Test DELETE method to delete an another organizer. Only admin should be able to delete another user. Another user can't delete another user. """

        # Retrieve user and access token
        admin = admin_user(add_token=False)

        if user_type == 'authenticated_user':
            user = user(add_token=True) #signed in as user

        # DELETE request to remove the another organizer (admin)
        url = reverse_lazy('organizers-detail', kwargs={'pk': admin.id})
        response = api_client.delete(url)

        assert response.status_code == expected_response  # No content after successful deletion
