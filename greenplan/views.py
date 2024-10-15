
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Organizer, Address, Program, Event, Template
from .serializers import CreateEventSerializer, OrganizerSerializer, \
    AddressSerializer, ProgramSerializer, EventSerializer, MiniEventSerializer, TemplateSerializer, MiniTemplateSerializer
from .permissions import IsAdminOrReadonly

# Create your views here.


class OrganizerViewSet(ModelViewSet):
    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'type')

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

        raise Http404(
            'Organizer Not Found. Kindly create your organizer profile.')


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
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('title', 'events__title')
    search_fields = ('title', 'featured_event__title', 'events__title')

    def get(self, request, *args, **kwargs):
        programs = self.filter_queryset(Program.objects.all())
        serializer = self.get_serializer(programs, many=True)

        data = {
            'status': 'Success',
            'message': 'Programs with all the events that belong to them retrieved.',
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'status': 'Success',
            'message': 'Programs created.',
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {'request': self.request}


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
            return Response({'error': 'Program is linked to an events. Unlink the event to delete this program.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class EventApiView(GenericAPIView):
    """ provide endpoints get and post"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = ['title', 'program__title', 'city_or_state']
    search_fields = ('title', 'program__title')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateEventSerializer
        return EventSerializer

    def get_queryset(self):
        # getting what is used for the filtering
        user = self.request.user

        # Admin sees all the events
        if user.is_staff:
            return Event.objects.all()

        # Regular authenticated users see only their events and other people true event while unauthenticated see only public event

        return Event.objects.filter(Q(organizer_id=user.pk) | Q(
            is_private=False)).order_by('-is_private')

    def get(self, request, *args, **kwargs):
        events = self.get_queryset()  # self.filter_queryset(self.get_queryset())
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
        return Response(data={'status': 'Success', 'message': 'No event match for the filter'}, status=status.HTTP_404_NOT_FOUND)

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
                         'message': 'Event not created',
                         'errors': serializer.errors}
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        return {'request': self.request}


class EventDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EventSerializer
        return CreateEventSerializer

    def get_object(self):
        user = self.request.user
        pk = self.kwargs['pk']

        if user.is_staff:
            return get_object_or_404(Event, pk=pk)
        event = Event.objects.filter(id=pk, organizer_id=user.id).first()

        if event is None:
            raise Http404('Invalid event detail')
        return event


class TemplateLibraryApiView(GenericAPIView):
    '''This template view is for listing all template like a template library.'''
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        ''' Our staff can view all template while others can view template linked to them or public event'''
        user = self.request.user

        if user.is_staff:
            return Template.objects.all()

        return Template.objects.filter(Q(event__organizer_id=user.id) | Q(event__is_private=False))

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()  # Template.objects.all()
        serializer = self.get_serializer(qs, many=True)
        data = {
            "status": "success",
            "message": " Template retrieved successfully",
            'total_template': qs.count(),
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_201_CREATED)


class EventTemplateApiView(GenericAPIView):
    '''View to create and retrieve templates for a specific event.'''
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Retrieve templates based on user role and event ID.'''
        user = self.request.user
        event_pk = self.kwargs['event_pk']

        if user.is_staff:
            return Template.objects.filter(event_id=event_pk)
        return Template.objects.filter(event_id=event_pk, event__organizer_id=user.id)

    def get(self, request, *args, **kwargs):
        event_templates = self.get_queryset()
        total_event_template = event_templates.count()

        if total_event_template == 0:
            return Response({'status': 'error',
                             'message': 'Event does not exist or you are not the organizer'},
                            status=status.HTTP_404_NOT_FOUND)

        # we want to limit the occurrence of the event to appear only once,
        # we used a another template serializer and  get the event directly here.
        event_pk = self.kwargs['event_pk']
        event_data = get_object_or_404(Event, pk=event_pk)
        event = MiniEventSerializer(event_data)
        serializer = MiniTemplateSerializer(event_templates, many=True)

        data = {
            "status": "success",
            "message": " Event templates retrieved successfully",
            'total_event_template': event_templates.count(),
            'event_data': event.data,
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "status": "success",
            "message": " Template created successfully",
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {'user': self.request.user, 'event_pk': self.kwargs['event_pk']}


class EventTemplateDetailApiView(RetrieveUpdateDestroyAPIView):
    'Retrieve a specific template for a specific event. methods: get, update, delete'

    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        '''Retrieve templates based on user role and template ID.'''
        user = self.request.user
        event_pk = self.kwargs['event_pk']
        template_pk = self.kwargs['pk']

        if user.is_staff:
            return Template.objects.filter(id=template_pk,event_id=event_pk).first()
        return Template.objects.filter(id=template_pk, event_id=event_pk,event__organizer_id=user.id).first()

    def get(self, request, *args, **kwargs):
        event_templates = self.get_object()

        if event_templates is None:
            return Response({'status': 'error',
                             'message': 'Template does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(event_templates)
        data = {
            "status": "success",
            "message": " Event template retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

