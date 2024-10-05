from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Event, Organizer, Address
from .serializers import EventSerializer, CreateEventSerializer, OrganizerSerializer, \
    AddressSerializer

# Create your views here.

# class CreateView()

class EventApiView(ListCreateAPIView):
    # permission_classes = [IsAuthenticated]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateEventSerializer
        else:
            return EventSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Event.objects.select_related('organizer', 'program')

        # Admin sees all the events
        if user.is_staff:
            return qs

        # Regular authenticated users see only their events
        if user.is_authenticated:
            return qs.filter(organizer_id=user.pk)

        # If no events found or user isn't authenticated
        return qs.filter(is_private=False)

    def get(self, request, *args, **kwargs):
        events = self.get_queryset()
        total_events = events.count()

        serializer = self.get_serializer(events, many=True)
        data = {
            "status": "Success",
            "message": "Events retrieved successfully",
            'total_events': total_events,
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            serializer = EventSerializer(
                serializer, context={'request': request})
            data = {
                "status": "success",
                "message": " Event Created successfully",
                "data": serializer.data
            }

            return Response(data, status=status.HTTP_201_CREATED)
        error_message = {'status': 'failed',
                         'message': 'Event not created'}
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        return {'request': self.request}


class OrganizerApiView(ListCreateAPIView):
    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pk = user.pk
        qs = Organizer.objects.all()

        if user.is_staff:
            return qs

        return qs.filter(pk=pk)

    def get_serializer_context(self):
        return {'request': self.request}


class OrganizerDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        user = self.request.user
        organizer = get_object_or_404(Organizer, pk=pk)

        # Our staff can view everyone profile"""
        if user.is_staff:
            return organizer

        # A user can view their profile
        if str(user.id) == pk:
            return organizer
        return PermissionDenied('You do not have permission to access this profile.')


class AddressApiView(ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        qs = Address.objects.select_related(
            'organizer').filter(organizer_id=pk)

        if user.is_staff:
            return qs
        if str(pk) == user.id:
            return qs
        return PermissionDenied('You do not have permission to access this Address.')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'status': 'Success',
            'message': 'Address created successfully.',
            'data': serializer.data
        }

        return Response(data=data, status=status.HTTP_201_CREATED)
    
    def get_serializer_context(self):
        return {'request': self.request}


class AddressDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs['pk']
        user = self.request.user

        address = get_object_or_404(Address,pk=pk)

        if user.is_staff:
            return address
        
        if str(user.id) == address.organizer.id:
            return address
        return PermissionDenied('You do not have permission to access this profile.')

 
