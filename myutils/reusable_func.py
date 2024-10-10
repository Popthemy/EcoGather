from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status


def get_jwt_tokens(user):
    """Get both the refresh and access token for user"""

    try:
        token = RefreshToken.for_user(user=user)

        return {
            'access': str(token.access_token),
            'refresh': str(token)
        }

    except TokenError as e:
        data = {'status': 'error', 'message': str(e)}
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
