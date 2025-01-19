from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q,Count
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated

from greenplan.documentation.greenplan.schemas import clone_template_doc

from .models import Organizer, Address, Program, Event, Template, CustomField
from .serializers import CreateEventSerializer, OrganizerSerializer, \
    AddressSerializer, ProgramSerializer, MiniProgramSerializer, EventSerializer, \
    MiniEventSerializer, TemplateSerializer, MiniTemplateSerializer, CustomFieldSerializer
from .permissions import IsAdminOrReadonly, IsOwnerOrReadOnly, IsOrganizerOwnerOrReadOnly, IsEventOwnerOrReadOnly, IsTemplateOwnerOrReadOnly
from .utils import track_impression
from .tasks import all_event_organizer_email

# Create your views here.

class OrganizerViewSet(ModelViewSet):
    '''This endpoint doesn't allow `POST` because new organizer is created when a new user is created by a signal.
    Anonymous user should be able to view the organizer but not allowed to perform other action. 
    Only the real organizer or admin can perform edit operations'''

    serializer_class = OrganizerSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    http_method_names = ['get', 'put', 'patch', 'delete']
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ('type',)
    search_fields = ('username', 'type')

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = self.request.user

        if user.is_staff and not pk:
            return Organizer.objects.annotate(event_count=Count('events'))

        # for non-admin it serve as details view, while it requires id for anonymous user
        id = pk if pk else user.id
        organizer = Organizer.objects.annotate(event_count=Count('events')).filter(pk=id)
        if organizer is not None:
            return organizer

        raise Http404(
            'Organizer Not Found! Try Again.')


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
        serializer.is_valid(raise_exception=True)  # raise 400
        serializer.save()

        data = {
            'status': 'Success',
            'message': 'Address created successfully.',
            'data': serializer.data
        }

        return Response(data=data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {'request': self.request, 'addresses_owner': self.kwargs.get('organizer_pk')}


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
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'program__title', 'organizer__username')
    ordering_fields = ('title',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateEventSerializer
        return MiniEventSerializer

    def get_queryset(self):

        # ### RUNNING CELERY TASK
        # task = all_event_organizer_email.delay()
        # print(f'task.id:{task.id}')

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
    permission_classes = (IsEventOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EventSerializer
        return CreateEventSerializer

    def get_object(self):
        user = self.request.user
        pk = self.kwargs['event_pk']

        event = get_object_or_404(Event, pk=pk)
        track_impression(self.request,event)

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
    permission_classes = (IsEventOwnerOrReadOnly,)

    def get_queryset(self):
        ''' Retrieve templates based on organizer of the event or the event is public.'''
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
    permission_classes = (IsEventOwnerOrReadOnly,)

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
    '''Retrieves all and create custom fields for a specific template.
    {
    "label": "opening prayer 1",
    "content": "i will demonstratre",
    "start_time": null,
    "end_time": null
    }
    '''
    permission_classes = (IsTemplateOwnerOrReadOnly, )
    serializer_class = CustomFieldSerializer

    def get_queryset(self):
        template_pk = self.kwargs['template_pk']
        user = self.request.user

        templates =  CustomField.objects.filter(template_id=template_pk)
        if not user.is_staff:
            templates = templates.filter(
                Q(template__event__organizer_id=user.id) | 
                Q(template__event__is_private=False)
                )
        return templates
    
    def post(self, request, *args, **kwargs):
        data = request.data
        is_bulk = isinstance(data,(list,tuple))

        serializer = self.get_serializer(data=data,many=is_bulk)
        if serializer.is_valid():
            serializer.save()

            message =  "Custom fields created successfully" if is_bulk else "Custom field created successfully"
            data = {
                'status':'Success',
                'message': message,
                'data': serializer.data
            }
            return Response(data,status=status.HTTP_201_CREATED)


        return super().post(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        template_pk = self.kwargs['template_pk']
        event = get_object_or_404(Event, templates=template_pk)
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
    permission_classes = (IsTemplateOwnerOrReadOnly, )
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



class CloneTemplateView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    @clone_template_doc
    def get(self,*args, **kwargs):
        '''The template to be cloned ID is gotten from the url.
        This only clone for template without paying attention to the event. '''

        template_id = kwargs['template_id']
        if template_id < 1:
            data = {
                "status": "error",
                "message": " Templates cloned unsuccessfully",
                "data": "ID can't be negative or less than one"}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

        template = get_object_or_404(Template,pk= template_id)

        try:
            duplicate = template.clone_template(user=Organizer.objects.get(user_id=self.request.user.id))
            serializer = MiniTemplateSerializer(duplicate)

            data = {
                "status": "success",
                "message": " Templates cloned successfully",
                "data": serializer.data }

            return Response( data,status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(data={
                'status':'error',
                'message': str(e)
            },status=status.HTTP_400_BAD_REQUEST)


