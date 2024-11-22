from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from greenplan.models import Organizer,Address
from model_bakery import baker
import pytest


User = get_user_model()


# ---------- List view -----------

# @pytest.mark.skip
@pytest.mark.django_db
class TestRetreiveAddress:

    # Positive test: 'GET' address list for all
    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_if_address_list_no_addresses_returns_404(self, api_client, user, admin_user, user_type):
        """ Test retrieving the list of addresses. Everyone can sees all organizer addresses.
        In a way this test for two scenario - When non admin tries to retrieve someone else and i try to retrieve for myself."""

        # Arrange
        admin = admin_user(add_token=True)

        if user_type == 'authenticated_user':
            user(add_token=True)

        url = reverse_lazy('addresses', kwargs={'organizer_pk': admin.id})

        # Action
        response = api_client.get(url)

        # Assert
        assert response.status_code == 404

    def test_if_anonymous_address_list_no_addresses_returns_404(self, api_client, admin_user):
        """ Test retrieving the list of addresses. Everyone can sees all organizer addresses even anonymous user."""

        # Arrange
        admin = admin_user(add_token=False)

        url = reverse_lazy('addresses', kwargs={'organizer_pk': admin.id})

        # Action
        response = api_client.get(url)

        # Assert
        assert response.status_code == 404

    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_if_address_list_returns_200(self, api_client, user, admin_user, user_type):
        """ Test retrieving the list of addresses. Everyone can sees all organizer addresses.
        In a way this test for two scenario - When non admin tries to retrieve someone else and i try to retrieve for myself.,
        An addition is we created an address for the user we are retrieving the address. """

        # Arrange
        admin = admin_user(add_token=True)

        address = baker.make(Address,organizer_id=admin.id)

        if user_type == 'authenticated_user':
            user(add_token=True)

        url = reverse_lazy('addresses', kwargs={'organizer_pk': admin.id})

        # Action
        response = api_client.get(url)
        print(f'User has an address already: {response.data}')

        # Assert
        assert response.status_code == 200

    def test_if_anonymous_address_list_returns_200(self, api_client, admin_user):
        """ Test retrieving the list of addresses. Everyone can sees all organizer addresses even anonymous user."""

        # Arrange
        admin = admin_user(add_token=False)

        url = reverse_lazy('addresses', kwargs={'organizer_pk': admin.id})
        address = baker.make(Address,organizer_id=admin.id)

        # Action
        response = api_client.get(url)

        # Assert
        assert response.status_code == 200

    # negative test: Invalid Id
    @pytest.mark.parametrize('user_type', ['anonymous','admin', 'authenticated_user'])
    def test_if_invalid_id_address_list_returns_400(self, api_client, user, admin_user, user_type):
        """ Test retrieving the list of addresses of an invalid_id """

        # Arrange
        invalid_id = '54ffdb95-45bb-4e6e-bf26-0b876bda2ab0'

        if user_type == 'admin':
            admin_user(add_token=True)
        if user_type == 'authenticated_user':
            user(add_token=True)

        url = reverse_lazy('addresses', kwargs={'organizer_pk': invalid_id})

        # Action
        response = api_client.get(url)
        print(f'invalid get address: {response.data}')

        # Assert
        assert response.status_code != 200


# @pytest.mark.skip
@pytest.mark.django_db
class TestCreateAddress:

    # Positive test: Create a new address (POST)
    @pytest.mark.parametrize('user_type', ['authenticated_user','admin'])
    def test_create_address_returns_201(self, api_client, user, admin_user, user_type):
        """ Test creating a new address by an admin and also by the user. Admin and authenticated users should be able to create an address for themselves."""

        # Arrange
        user = user(add_token=True)

        if user_type == 'admin': # attach the admin token
            admin_user(add_token=True)

        data = {
            'street_number': 12,
            'street_name': 'Pytest',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
            'country': 'Nigeria'
        }

        # Action
        url = reverse_lazy('addresses', kwargs={'organizer_pk': user.id})
        response = api_client.post(url, data)
        # print(f'creating address {response.data}')

        # Assert
        assert response.status_code == 201
        assert response.data['data']['street_name'] == data['street_name']


    #negative test
    def test_if_anonymous_create_address_returns_401(self, api_client, user):
        """ Test creating a new address. Admin and authenticated users should be able to create an address. """
        
        # Arrange
        current_user = user(add_token=False) # no token is attached 

        data = {
            'street_number': 12,
            'street_name': 'Pytest',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
            'country': 'Nigeria'
        }

        # Action
        url = reverse_lazy('addresses', kwargs={'organizer_pk': current_user.id})
        response = api_client.post(url, data)
        print(f'creating address {response.data}')

        # Assert
        assert response.status_code == 401


    @pytest.mark.parametrize('user_type,expected_response', [('anonymous',401),('admin',400), ('authenticated_user',403)])
    def test_if_address_invalid_id_returns(self, api_client, user, admin_user, user_type,expected_response):
        """ Test creating a new address. Admin and authenticated users, should not be able to create 
        an address for other users whether they exist or not. """

        # Arrange
        invalid_id = '54ffdb95-45bb-4e6e-bf26-0b876bda2a09'

        current_user = ''

        if user_type == 'admin':
            current_user = admin_user(add_token=True)

        if user_type == 'authenticated_user':
            current_user = user(add_token=True)

        data = {
            'street_number': 12,
            'street_name': 'Pytest',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
            'country': 'Nigeria'
        }

        # Action
        url = reverse_lazy('addresses', kwargs={'organizer_pk': invalid_id})
        response = api_client.post(url, data)
        print(f'creating address with invalid id  {response.data}')

        # Assert
        assert response.status_code == expected_response


# ---------- Detail view -----------

# @pytest.mark.skip
@pytest.mark.django_db
class TestRetrieveAddress:

    # Positive test: Retrieve address details
    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_get_address_detail_returns_200(self, api_client, user, admin_user, user_type):
        """ Test retrieving an individual address. Admin and  authenticated. """

        # Arrange
        user = user(add_token=True)
        
        if user_type == 'admin':
            user = admin_user(add_token=True)

        address = baker.make(Address,organizer_id=user.id)

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': user.id})

        # Action
        response = api_client.get(url)

        # Assert
        assert response.status_code == 200
        assert response.data['street_name'] == address.street_name


    def test_get_address_detail_by_anonymous_returns_200(self, api_client, user):
        """ Test retrieving an individual address by an anonymous user."""

        # Arrange
        user = user(add_token=False)

        address = baker.make(Address,organizer_id=user.id)

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': user.id})

        # Action
        response = api_client.get(url)

        # Assert
        assert response.status_code == 200
        assert response.data['street_name'] == address.street_name

    # Negative test: Retrieve address detail with invalid ID
    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_invalid_id_get_address_detail_returns_404(self, api_client, user, admin_user, user_type):
        """ Test retrieving an individual address. Admin and  authenticated. """

        # Arrange
        user = user(add_token=True)
        
        if user_type == 'admin':
            user = admin_user(add_token=True)

        url = reverse_lazy('address-detail', kwargs={'pk': 1, 'organizer_pk': user.id})

        # Action
        response = api_client.get(url)
        print(f'invalid address id: {response.data}')

        # Assert
        assert response.status_code == 404


    def test_invalid_id_get_address_detail_by_anonymous_returns_404(self, api_client, user):
        """ Test retrieving an individual address with invalid ID by an anonymous user."""

        # Arrange
        user = user(add_token=False)

        address = baker.make(Address,organizer_id=user.id)

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': user.id})

        # Action
        response = api_client.get(url)

        # Assert
        assert response.status_code == 200


# @pytest.mark.skip
@pytest.mark.django_db
class TestUpdateAddress:
    # Positive test: Update address details (PATCH)
    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_patch_address_returns_200(self, api_client, user, admin_user, user_type):
        """ Test updating address details. Admin or the address owner can update the address. """
        
        # Arrange
        update_data = {'street_name': 'updated street (New St.)'}
        
        user = user(add_token=True)
        
        if user_type == 'admin':
            # this way an admin also update for a authenticated user
            admin_user(add_token=True)

        address = baker.make(Address,organizer_id=user.id) #make address for a user

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': user.id})


        # Action
        response = api_client.patch(url, update_data)

        # Assert
        assert response.status_code == 200
        assert response.data['street_name'] == update_data['street_name']


    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_put_address_returns_200(self, api_client, user, admin_user, user_type):
        """ Test updating address details. Admin or the address owner can update the address. """
        
        # Arrange
        
        user = user(add_token=True)
        
        if user_type == 'admin':
            # this way an admin also update for a authenticated user
            admin_user(add_token=True)

        address = baker.make(Address,organizer_id=user.id) #make address for a user
        update_data = {
            'street_name': 'updated street (New St.)',
            'street_number':address.street_number,
            'city':address.city,
            'state':address.state,
            'country':address.country,
            }

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': user.id})


        # Action
        response = api_client.put(url, update_data)

        # Assert
        assert response.status_code == 200
        assert response.data['street_name'] == update_data['street_name']


    # negative test
    @pytest.mark.parametrize('missing_data', ['street_number', 'street_name','city','state','country'])
    def test_put_invalid_data_address_returns_400(self, api_client, user, missing_data):
        """ Test updating address details. Admin or the address owner can update the address with incomplete data. """
        
        # Arrange
        user = user(add_token=True)
        address = baker.make(Address,organizer_id=user.id) # make address for a user

        update_data = {
            'street_name': 'updated street (New St.)',
            'street_number':address.street_number,
            'city':address.city,
            'state':address.state,
            'country':address.country,
            }        
        
        if missing_data in update_data:
            update_data[missing_data] = ''

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': user.id})

        # Action
        response = api_client.put(url, update_data)
        print(response.data)

        # Assert
        assert response.status_code == 400
        assert  missing_data in response.data


    def test_patch_by_anonymous_address_returns_401(self, api_client, user):
        """ Test updating address details. Admin or the address by non-owner """
        
        # Arrange
        update_data = {'street_name': 'updated street (New St.)'}
        
        user = user(add_token=False)

        address = baker.make(Address,organizer_id=user.id) #make address for a user

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': user.id})

        # Action
        response = api_client.patch(url, update_data)

        # Assert
        assert response.status_code == 401


@pytest.mark.django_db
class TestDeleteAddress:

    @pytest.mark.parametrize('user_type', ['admin', 'authenticated_user'])
    def test_patch_address_returns_204(self, api_client, user, admin_user, user_type):
        """ Test deleting address . Admin or the address owner can delete the address. """
        
        # Arrange        
        user = user(add_token=True)
        
        if user_type == 'admin':
            # this way an admin also update for a authenticated user
            admin_user(add_token=True)

        address = baker.make(Address,organizer_id=user.id) #make address for a user

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': user.id})

        # Action
        response = api_client.delete(url)
        print(response.data)

        # Assert
        assert response.status_code == 204
        assert response.data == None

        
    # Negative test: Delete address as a non-owner
    @pytest.mark.parametrize('user_type,code',[('anonymous',401),('authenticated_user',403)])
    def test_delete_address_not_owner_returns_403(self, api_client, user, admin_user,user_type,code):
        """ Test deleting an address as a non-owner. Should return 403 Forbidden.  """

        address_owner = admin_user(add_token=False)
        address = baker.make(Address,organizer_id=address_owner.id) # make address for a user

        if user_type == 'authenticated_user':
            user(add_token=True) #attach authenticated token to header

        url = reverse_lazy('address-detail', kwargs={'pk': address.id, 'organizer_pk': address_owner.id})
        response = api_client.delete(url)

        assert response.status_code == code

