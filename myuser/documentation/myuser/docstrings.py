from drf_spectacular.utils import OpenApiExample


REGISTER_USER_DESCRIPTION = """
    User registration endpoint.

    This endpoint allows new, unauthenticated users to register by providing necessary user information.
    The `IsAnonymous` permission class ensures that only unauthenticated users can access this endpoint.
    If a user is already authenticated, they will be denied access.

    **Permissions**:
        - `IsAnonymous`: Only unauthenticated users are allowed to register.
    """


REGISTER_USER_CREATED = OpenApiExample(
    '201 CREATED',
    description='Registration Successful',
    value={'data': {
        'status': 'Success',
        'message': 'Registration Successful',
        "token": {
            "access": "your-access-token-here",
            "refresh": "your-refresh-token-here"
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
    description="If the data is invalid, the serializer will raise an exception, and an appropriate error response will be returned.",
    value={'errors': {"username": ["This field is required."],
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


LOGIN_VIEW_DESCRIPTION = """
    User login endpoint.

    This endpoint allows authenticated users to log in by providing their credentials. 
    The `IsAnonymous` permission class ensures that only unauthenticated users can register through the registration endpoint, 
    but this login endpoint should be used by authenticated users or users trying to log in.

    **Permissions**:
        - `IsAnonymous`: Ensures that only unauthenticated users can access the registration endpoint.
"""


LOGIN_USER_200_OK = OpenApiExample(
    '200 OK',
    description="If the provided credentials are valid, a successful login will return a JWT token and user data.",
    value={
        'status': 'Success',
        'message': 'Welcome back👋',
        "token": {
            "access": "your-access-token-here",
            "refresh": "your-refresh-token-here"
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


LOGOUT_USER_DESCRIPTION = """
    User logout endpoint.

    This endpoint allows authenticated users to log out by invalidating their refresh token.
    The refresh token is blacklisted so that it cannot be used to generate new access tokens.
    However, the user will not be immediately logged out until the access token has expired.
    After the access token expires, the user must log in again to obtain new tokens.

    **Permissions**:
        - `IsAuthenticated`: Only authenticated users (with a valid token) are allowed to log out.
"""


LOGOUT_USER_200_OK = OpenApiExample(
    '200 OK',
    description="If the refresh token is valid and successfully blacklisted, you can't generate a new access token with that token anymore.",
    value={
        'status': 'Success',
        'message': "Token blacklisted, you can't generate a new access token with that token 😋"
    },
    response_only=True,
    status_codes=['200']
)


LOGOUT_USER_400_BAD_REQUEST = OpenApiExample(
    '400 BAD_REQUEST',
    description="If the refresh token is invalid or the logout operation fails, the response will indicate an error.",
    value={
        'status': 'Error',
        'message': 'Logout failed',
        'details': 'Invalid refresh token'
    },
    response_only=True,
    status_codes=['400']
)


TOKEN_REFRESH_DESCRIPTION = """
    Token refresh endpoint.

    This endpoint allows a user to refresh their access token after it has expired, by providing a valid refresh token. 
    The refresh token is used to obtain a new access token without requiring the user to log in again. 
    If the provided refresh token is invalid or expired, an error will be returned.
"""

TOKEN_REFRESH_200_OK = OpenApiExample(
    '200 OK',
    description="If the provided refresh token is valid, a new access token is issued successfully.",
    value={
        'status': 'Success',
        'message': 'Token refreshed successfully.',
        'access_token': 'new-access-token-here'
    },
    response_only=True,
    status_codes=['200']
)


TOKEN_REFRESH_400_BAD_REQUEST = OpenApiExample(
    '400 BAD_REQUEST',
    description="If the provided refresh token is invalid or expired, the token refresh will fail.",
    value={
        'status': 'Error',
        'message': 'Token refresh failed',
        'details': 'Refresh token is invalid or expired.'
    },
    response_only=True,
    status_codes=['400']
)
