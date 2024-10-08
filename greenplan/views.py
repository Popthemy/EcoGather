from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.generics import GenericAPIView,ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import  Organizer, Address,Program, Event
from .serializers import  CreateEventSerializer, OrganizerSerializer, \
    AddressSerializer,ProgramSerializer, EventSerializer
from .permissions import IsAuthenticatedOrReadonly

# Create your views here.

class OrganizerViewSet(ModelViewSet):
    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = self.request.user

        if user.is_staff:
            organizer = Organizer.objects.filter(pk=pk)
            if pk and organizer is not None:
                return organizer
            return Organizer.objects.all()
        
        organizer = Organizer.objects.filter(pk=user.id)
        if organizer is not None:
            return organizer

        raise Http404('Organizer Not Found. Kindly create your organizer profile.')


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
        address = Address.objects.filter(pk=pk)

        if user.is_staff:
            return address.first()
        address = address.filter(organizer__email=user.email).first()
        if address is None:
            raise Http404('Address Not Found')
        return address


class ProgramApiView(GenericAPIView):
    serializer_class = ProgramSerializer

    def get(self,request):
        programs = Program.objects.all()
        serializer = self.get_serializer(programs, many=True)

        data = {
            'status':'Success',
            'message': 'Programs with all the events that belong to them retrieved.',
            'data': serializer.data
        }

        return Response(data,status=status.HTTP_200_OK)




class EventApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadonly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateEventSerializer
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
