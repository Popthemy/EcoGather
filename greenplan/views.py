from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Event, Organizer, Address
from .serializers import EventSerializer, CreateEventSerializer, OrganizerSerializer, \
    AddressSerializer

# Create your views here.

# class CreateView()


class OrganizerViewSet(ModelViewSet):
    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = self.request.user

        if user.is_staff:
            if pk:
                return Organizer.objects.filter(pk=pk)
            return Organizer.objects.all()

        return Organizer.objects.filter(pk=user.id)


class AddressApiView(ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get('pk')

        if user.is_staff and pk:
            return Address.objects.filter(organizer_id=pk)

        return Address.objects.filter(organizer_id=user.id)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
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
        qs = Address.objects.filter(pk=pk)

        if user.is_staff:
            return qs.first()
        return qs.filter(organizer__email=user.email).first()


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
