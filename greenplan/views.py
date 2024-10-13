
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status,filters
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .models import  Organizer, Address,Program, Event
from .serializers import  CreateEventSerializer, OrganizerSerializer, \
    AddressSerializer,ProgramSerializer, EventSerializer
from .permissions import IsAdminOrReadonly

# Create your views here.

class OrganizerViewSet(ModelViewSet):
    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username','type')

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
    permission_classes = [IsAdminOrReadonly]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    filterset_fields = ('title','events__title')
    search_fields = ('title','featured_event__title','events__title')

    def get(self,request,*args, **kwargs):
        programs = self.filter_queryset(Program.objects.all())
        serializer = self.get_serializer(programs, many=True)

        data = {
            'status':'Success',
            'message': 'Programs with all the events that belong to them retrieved.',
            'data': serializer.data
        }

        return Response(data,status=status.HTTP_200_OK)
    
    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'status':'Success',
            'message': 'Programs created.',
            'data': serializer.data
        }

        return Response(data,status=status.HTTP_201_CREATED)
    
    def get_serializer_context(self):
        return {'request':self.request}


class ProgramDetailApiView(RetrieveUpdateDestroyAPIView):
    """Provide functionality:
    get: for all users
    put/patch and delete for admin users """

    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadonly]


    def destroy(self, request, *args, **kwargs):
        """We shouldn't delete program that have events linked to them so we raise an error."""
        
        # pk = self.kwargs['pk']
        # program = get_object_or_404(Program,pk=pk)
        program = self.get_object()
        print(f'event:{ program.events }')
        if program.events.count() > 0:
            return Response({'error':'Program is linked to an events. Unlink the event to delete this program.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class EventApiView(ListCreateAPIView):
    """ provide endpoints get and post"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    filterset_fields = ['title', 'program__title', 'city_or_state']
    search_fields = ('title','program__title')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateEventSerializer
        return EventSerializer

    def get_queryset(self):
        # getting what is used for the filtering
        user = self.request.user
        qs = Event.objects.all()

        # Admin sees all the events
        if user.is_staff:
            return qs

        # Regular authenticated users see only their events
        if user.is_authenticated:
            return  qs.filter(Q(organizer_id=user.pk) | Q(
                is_private=False)).order_by('-is_private')

        # If no events found or user isn't authenticated
        return  qs.filter(is_private=False)
    

    def get(self, request, *args, **kwargs):
        events = self.filter_queryset(self.get_queryset())
        total_events = events.count()

        serializer = self.get_serializer(events, many=True)
        if len(serializer.data) > 0:

            data = {
                "status": "Success",
                "message": "Events retrieved successfully",
                'total_events': total_events,
                "data": serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)
        return Response(data=('No Match'), status=status.HTTP_404_NOT_FOUND)

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

