from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from .permissions import IsAnonymous

# Create your views here.

User = get_user_model()


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAnonymous]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'status': 'Success',
            'message': 'Registration Successful',
            'data': serializer.data
        }

        return Response(data=data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAnonymous]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.login_user(serializer.validated_data)

        if user:
            serializer = UserSerializer(user)

            data = {
                'status': 'Success',
                'message': 'Login in successful',
                'data': serializer.data
            }
            return Response(data=data, status=status.HTTP_200_OK)
        
        return Response(data={
            'status': 'Error',
            'message': 'Login Unsuccessful',
            'data': serializer.errors},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# class LogoutView(GenericAPIView):
    