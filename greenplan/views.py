
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Organizer, Address, Program, Event, Template, CustomField
from .serializers import CreateEventSerializer, OrganizerSerializer, \
    AddressSerializer, ProgramSerializer, MiniProgramSerializer, EventSerializer, MiniEventSerializer, TemplateSerializer, MiniTemplateSerializer, CustomFieldSerializer
from .permissions import IsAdminOrReadonly, IsOrganizerOrReadOnly,IsOrganizerOwnerOrReadOnly
from .task import all_event_organizer_email
# Create your views here.


class OrganizerViewSet(ModelViewSet):
    '''This endpoint doesn't allow `POST` because new organizer is created when a new user is created by a signal.
    Anonymous user should be able to view the organizer but not allowed to perform other action. 
    Only the real organizer or admin can perform edit operations'''

    serializer_class = OrganizerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'type')

    def get_permissions(self):
        request = self.request
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOrganizerOrReadOnly]
        return super().get_permissions()

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = self.request.user

        if user.is_staff and not pk:
            # print(f'@@@@@@  admin request -> admin:{user.id}')
            return Organizer.objects.all()

        # print(
        #     f'!!!! Ordinary user request -> user: {user.id} , request id: {pk}')

        # this will act as the detail view for admin user , also list for non-admin
        id = pk if pk else user.id
        organizer = Organizer.objects.filter(pk=id)
        if organizer is not None:
            return organizer

        raise Http404(
            'Organizer Not Found. Kindly create your organizer profile.')


class AddressApiView(ListCreateAPIView):
    ''' Method: Get and Post 
     {
        "street_number": 15,
        "street_name": "Ahmadu Bello",
        "city": "Kano",
        "state": "Abuja",
        "country": "Nigeria"
    }'''

    serializer_class = AddressSerializer
    permission_classes = (IsOrganizerOwnerOrReadOnly, )

    def get_queryset(self):
        org_pk = self.kwargs.get('organizer_pk')

        addresses = Address.objects.filter(organizer_id=org_pk)

        if not addresses:
            raise Http404("Address not found for the user")

        return addresses

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # raise 400
        serializer.save()

        data = {
            'status': 'Success',
            'message': 'Address created successfully.',
            'data': serializer.data
        }

        return Response(data=data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {'request': self.request,'addresses_owner': self.kwargs.get('organizer_pk') }


class AddressDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsOrganizerOwnerOrReadOnly,)

    def get_object(self):
        pk = self.kwargs['pk']
        org_pk = self.kwargs.get('organizer_pk')

        return get_object_or_404(Address, pk=pk, organizer__user_id=org_pk)

class ProgramApiView(GenericAPIView):
    '''This program view give the list of event group into their types.
    Only Admin is allowed to create new program.'''

    queryset = Program.objects.all()
    serializer_class = MiniProgramSerializer
    permission_classes = [IsAdminOrReadonly]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('title',)
    search_fields = ('title', 'featured_event__title')

    def get(self, request, *args, **kwargs):
        programs = self.filter_queryset(self.get_queryset())
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
    put/patch and delete for admin"""

    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadonly]

    def get_object(self):
        return get_object_or_404(Program, pk=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        """We shouldn't delete program that have events linked to them so we raise an error."""

        program = self.get_object()
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

        ### RUNNING CELERY TASK
        task = all_event_organizer_email.delay()
        print(f'task.id:{task.id}')
        
        # getting what is used for the filtering
        user = self.request.user

        # Admin sees all the events
        if user.is_staff:
            return Event.objects.all()

        # Regular authenticated users see only their events and other people true event
        # while unauthenticated see only public event

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
        serializer.is_valid(raise_exception=True)
        serializer = serializer.save()
        serializer = EventSerializer(
            serializer, context={'request': request})
        data = {
            "status": "success",
            "message": " Event Created successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {'request': self.request}


class EventDetailApiView(RetrieveUpdateDestroyAPIView):
    '''This view allows get for everyone while restricting update only to admin and organizer '''
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        request = self.request
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOrganizerOrReadOnly]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EventSerializer
        return CreateEventSerializer

    def get_object(self):
        user = self.request.user
        pk = self.kwargs['pk']

        event = get_object_or_404(Event, pk=pk)

        if event.organizer.user == user or user.is_staff:
            return event

        if not event.is_private:
            return event
        raise PermissionDenied(
            "You don't have permission to access this Event.")


class TemplateLibraryApiView(GenericAPIView):
    '''This template view is for listing all template like a template library.'''
    serializer_class = TemplateSerializer

    def get_queryset(self):
        ''' Staff can view all template while others can view template linked to them or public event'''
        user = self.request.user

        if user.is_staff:
            return Template.objects.all()

        return Template.objects.filter(Q(owner_id=user.id) | Q(event__is_private=False) | Q(event__isnull=True))

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()

        serializer = self.get_serializer(qs, many=True)
        data = {
            "status": "success",
            "message": " Template retrieved successfully",
            'total_template': qs.count(),
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_201_CREATED)


class EventTemplateApiView(GenericAPIView):
    '''View to create and retrieve (list_createview) templates for a specific event.'''
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        '''Allow only staff and organizer to create template for an event'''
        if self.request.method == 'POST':
            self.permission_classes = [IsOrganizerOrReadOnly]
        return super().get_permissions()

    def get_queryset(self):
        '''Retrieve templates based on organizer of the event or the event is  public.'''
        user = self.request.user

        event_pk = self.kwargs['event_pk']
        event = get_object_or_404(Event, pk=event_pk)

        if user.is_staff or (event.organizer.user == user):
            return event.templates.all()

        if not event.is_private:
            return event.templates.all()
        # Since the event is private then the template shouldn't be revealed
        raise PermissionDenied(
            "You don't have permission to access templates for this event.")

    def get(self, request, *args, **kwargs):
        event_templates = self.get_queryset()

        total_event_template = event_templates.count()

        # event_pk = self.kwargs['event_pk']
        # event_data = get_object_or_404(Event, pk=event_pk)
        # event = MiniEventSerializer(event_data)
        serializer = MiniTemplateSerializer(event_templates, many=True)

        data = {
            "status": "success",
            "message": " Event templates retrieved successfully",
            'total_event_template': event_templates.count(),
            # 'event_data': event.data,
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


class EventTemplateDetailApiView(GenericAPIView):
    'Retrieve a specific template for a specific event. methods: get, update, delete'

    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """ Allow admin or organizer to perform full actions"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOrganizerOrReadOnly]
        return super().get_permissions()

    def get_queryset(self):
        '''Retrieve templates based on user role and template ID.'''
        user = self.request.user
        event_pk = self.kwargs['event_pk']
        template_pk = self.kwargs['pk']

        event = get_object_or_404(Event, pk=event_pk)

        if user.is_staff or event.organizer.user == user:
            return get_object_or_404(Template, pk=template_pk)

        if not event.is_private:
            return get_object_or_404(Template, pk=template_pk)

        # Since the event is private then the template shouldn't be revealed
        raise PermissionDenied(
            "You don't have permission to access templates for this event.")

    def get(self, request, *args, **kwargs):
        event_templates = self.get_queryset()

        serializer = self.get_serializer(event_templates)
        data = {
            "status": "success",
            "message": " Event template retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_queryset()

        serializer = self.get_serializer(
            instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "status": "success",
            "message": " Template fully updated successfully",
            "data": serializer.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "status": "success",
            "message": " Template partailly updated successfully",
            "data": serializer.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        template = self.get_queryset()
        event_pk = self.kwargs['event_pk']
        user = self.request.user

        event = get_object_or_404(Event, pk=event_pk)
        if not user.is_staff and event.organizer.user != user:
            raise PermissionDenied(
                'You are not the organizer of this event ')

        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        return {'user': self.request.user, 'event_pk': self.kwargs['event_pk']}


class CustomFieldApiView(ListCreateAPIView):
    '''Retrieves all custom fields for a specific template.'''
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CustomFieldSerializer

    def get_queryset(self):
        template_pk = self.kwargs['template_pk']
        user = self.request.user

        if user.is_staff:
            return CustomField.objects.filter(template_id=template_pk)

        return CustomField.objects.filter(
            (Q(template_id=template_pk) & Q(
                template__event__organizer_id=user.id)) | (Q(template_id=template_pk) & Q(template__event__is_private=False))
        )

    def get(self, request, *args, **kwargs):
        # 1, 9,4,10,13
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        template_pk = self.kwargs['template_pk']
        user = self.request.user
        event = get_object_or_404(Event, templates=template_pk)

        if event.is_private is True and event.organizer.user != user:
            raise PermissionDenied(
                'You are not allowed to access this template fields.')

        event_serializer = MiniEventSerializer(event)
        data = {
            "status": "success",
            "message": " Custom fields for the template retrieved successfully",
            'total_custom_fields_for_template': qs.count(),
            "event_data": event_serializer.data,
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {
            'template_pk': self.kwargs['template_pk'],
            'user': self.request.user,
        }


class CustomFieldDetailApiView(GenericAPIView):
    '''View to get ,edit and delete a custom fields based on role only user and staff can perform full operations'''
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CustomFieldSerializer

    def get_object(self):
        template_pk = self.kwargs['template_pk']
        pk = self.kwargs['pk']
        user = self.request.user

        if user.is_staff:
            return CustomField.objects.filter(id=pk, template_id=template_pk).first()
        custom_field = CustomField.objects.filter(id=pk, template_id=template_pk).filter(
            (Q(
                template__event__organizer_id=user.id)) | Q(template__event__is_private=False)).first()
        if not custom_field:
            raise Http404('Custom field not found')
        return custom_field

    def get(self, request, *args, **kwargs):
        custom_field = self.get_object()
        serializer = self.get_serializer(custom_field)
        data = {
            "status": "success",
            "message": " Templates custom field retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "status": "success",
            "message": " Templates custom field was updated successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        custom_field = self.get_object()
        template_pk = self.kwargs['template_pk']
        user = self.request.user

        event = get_object_or_404(Event, templates=template_pk)
        if not user.is_staff and event.organizer.user != user:
            raise PermissionDenied(
                'You are not the organizer of the event this field is linked to.')

        custom_field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        return {
            'template_pk': self.kwargs['template_pk'],
            'user': self.request.user,
        }
