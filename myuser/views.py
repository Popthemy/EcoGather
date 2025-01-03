from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView, TokenBlacklistView as BaseTokenBlacklistView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from myutils.reusable_func import get_jwt_tokens

from myuser.documentation.myuser.schemas import register_user_doc,login_user_doc,logout_user_doc,refresh_token_doc

from .serializers import UserSerializer, LoginSerializer, LogoutSerializer
from .permissions import IsAnonymous

# Create your views here.

User = get_user_model()


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAnonymous]
    
    @register_user_doc
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = get_jwt_tokens(user)

        data = {
            'status': 'Success',
            'message': 'Registration Successful',
            'token': token,
            'data': serializer.data
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAnonymous]

    @login_user_doc
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            user = self.login_user(serializer.validated_data)

            if user is not None:
                print(f'!!!!!!! I am the user{user}')
                serializer = UserSerializer(user)
                token = get_jwt_tokens(user)

                data = {
                    'status': 'Success',
                    'message': 'Welcome back👋',
                    'token': token,
                    'data': serializer.data
                }
                return Response(data=data, status=status.HTTP_200_OK)

        return Response(data={
            'status': 'Error',
            'message': 'Login Unsuccessful',
            'data': serializer.errors},
            status=status.HTTP_401_UNAUTHORIZED)

    def login_user(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user = authenticate(
            request=self.request, username=email, password=password)
        print(f'!!!!!!!login user{user}')

        return user



@refresh_token_doc
class TokenRefreshView(BaseTokenRefreshView):
    """ Allows a user to get new access token after their token has expired."""
    pass


class LogoutView(GenericAPIView):
    '''Log out a user through refresh token blacklist does not log them out immediately 
    until the access token has expired and they should login to get new tokens.'''

    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @logout_user_doc
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        refresh_token = request.data.get('refresh')

        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status": "Success", "message": "Token blacklisted, you can't generate a new access token with that token 😋"}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"status": "Error", "message": "Logout failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
