from drf_spectacular.utils import OpenApiResponse,OpenApiExample
from myuser.serializers import UserSerializer


REGISTER_USER_DESCRIPTION = """
    User registration endpoint.

    This endpoint allows new, unauthenticated users to register by providing necessary user information.
    The `IsAnonymous` permission class ensures that only unauthenticated users can access this endpoint.
    If a user is already authenticated, they will be denied access.

    **Permissions**:
        - `IsAnonymous`: Only unauthenticated users are allowed to register.
    """

LOGIN_VIEW_DESCRIPTION = """
    User login endpoint.

    This endpoint allows authenticated users to log in by providing their credentials. 
    The `IsAnonymous` permission class ensures that only unauthenticated users can register through the registration endpoint, 
    but this login endpoint should be used by authenticated users or users trying to log in.

    **Permissions**:
        - `IsAnonymous`: Ensures that only unauthenticated users can access the registration endpoint.
"""

REGISTER_USER_CREATED = OpenApiExample(
  '201 CREATED',
  description='Registration Successful',
  value={'data':{
            'status': 'Success',
            'message': 'Registration Successful',
             "token": {
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyOTc0MDMwLCJpYXQiOjE3MzI4ODc2MzAsImp0aSI6ImUxMDE4NTQ3MDhlODQxMTA5YWM0Y2FiOTA1Nzk2NmViIiwidXNlcl9pZCI6IjhlZjljNjVlLTUwOTMtNDdjMi04OWMzLWFiNDg5ZTRkMzQyNSJ9.zp3M-qO7OgnELMmkJ4sazauilaBYL-M38bEEyXfNPiE",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjk3NDAzMCwiaWF0IjoxNzMyODg3NjMwLCJqdGkiOiJhM2I3MWU0YmU4YmU0ZmYyYWJjMjc2ZDkyNTg3NmNhYSIsInVzZXJfaWQiOiI4ZWY5YzY1ZS01MDkzLTQ3YzItODljMy1hYjQ4OWU0ZDM0MjUifQ.64gFe_QBLrkCJNJu78jJDmRF0lEh1GjM43ykHerlBlY"
    },
    "data": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "email": "example@gmail.com"
    }
        }
  },
  response_only=True,
  status_codes=['201']
)


REGISTER_USER_BAD_REQUEST = OpenApiExample(
  '400 BAD_REQUEST',
  description= "If the data is invalid, the serializer will raise an exception, and an appropriate error response will be returned.",
  value={'errors':{"username": ["This field is required."],
                   "password": ["This field is required."],
                    "confirm_password": ["This field may not be blank."],
                    "field": ["Password too common. Use a strong password"],
                    "non_field_errors": [
                        "This password is too short.", "It must contain at least 8 characters.",
                        "Password and Confirm_password doesn't match."
                    ]
                    }},
    response_only=True,
    status_codes=['400']
)


LOGIN_USER_200_OK = OpenApiExample(
    '200 OK',
    description="If the provided credentials are valid, a successful login will return a JWT token and user data.",
    value={
        'status': 'Success',
        'message': 'Welcome back👋',
         "token": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyOTc0MDMwLCJpYXQiOjE3MzI4ODc2MzAsImp0aSI6ImUxMDE4NTQ3MDhlODQxMTA5YWM0Y2FiOTA1Nzk2NmViIiwidXNlcl9pZCI6IjhlZjljNjVlLTUwOTMtNDdjMi04OWMzLWFiNDg5ZTRkMzQyNSJ9.zp3M-qO7OgnELMmkJ4sazauilaBYL-M38bEEyXfNPiE",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjk3NDAzMCwiaWF0IjoxNzMyODg3NjMwLCJqdGkiOiJhM2I3MWU0YmU4YmU0ZmYyYWJjMjc2ZDkyNTg3NmNhYSIsInVzZXJfaWQiOiI4ZWY5YzY1ZS01MDkzLTQ3YzItODljMy1hYjQ4OWU0ZDM0MjUifQ.64gFe_QBLrkCJNJu78jJDmRF0lEh1GjM43ykHerlBlY"
    },
    "data": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "email": "example@gmail.com"
    }
    },
    response_only=True,
    status_codes=['200']
)



LOGIN_USER_401_UNAUTHORIZED = OpenApiExample(
    '401 UNAUTHORIZED',
    description="If the login credentials are invalid (e.g., incorrect username/password), an error response will be returned.",
    value={
        'status': 'Error',
        'message': 'Login Unsuccessful',
        'data': {
            'non_field_errors': [
                'Unable to log in with provided credentials.',
                'Invalid username or password.'
            ]
        }
    },
    response_only=True,
    status_codes=['401']
)
