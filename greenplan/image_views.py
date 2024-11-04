from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .models import OrganizerImage, EventImage
from .serializers import OrganizerImageSerializer, EventImageSerializer


class ListOrganizerImageApiView(GenericAPIView):
    """List all Organizer Images"""

    queryset = OrganizerImage.objects.all()
    serializer_class = OrganizerImageSerializer

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        data = {
            "status": "Success",
            "message": "Organizers image retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class OrganizerImageApiView(GenericAPIView):
    '''This view is for getting and creating organizer image.
    You can create image if your id matches the currently logged in user or you are a staff.'''

    serializer_class = OrganizerImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        '''Anyone can see organizer image'''
        organizer_pk = self.kwargs['organizer_pk']

        return OrganizerImage.objects.filter(organizer_id=organizer_pk)

    def get(self, request, *args, **kwargs):
        organizers_images = self.get_queryset()
        serializer = self.get_serializer(organizers_images, many=True)

        data = {
            "status": "Success",
            "message": "Organizers list of image retrieved.",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "status": "Success",
            "message": "New organizers image added successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {"user": self.request.user, "organizer_pk": self.kwargs["organizer_pk"]}


class OrganizerImageDetailApiView(RetrieveUpdateDestroyAPIView):
    '''This view is for getting, updating, and deleting a single image that belongs to an organizer'''

    serializer_class = OrganizerImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        organizer_pk = self.kwargs['organizer_pk']
        image_pk = self.kwargs['pk']

        if user.is_staff:
            return get_object_or_404(OrganizerImage, pk=image_pk)

        # Check if the user is the organizer of the image
        organizer_image = get_object_or_404(
            OrganizerImage, pk=image_pk, organizer_id=organizer_pk)

        if user.id != organizer_pk:
            raise PermissionDenied(
                "You do not have permission to access this image.")
        return organizer_image
    
    def destroy(self, request, *args, **kwargs):
        
        organizer_image = self.get_object()
        serializer = self.get_serializer(organizer_image)
        organizer_pk = self.kwargs['organizer_pk']
        serializer.validate_org_id(organizer_id=organizer_pk)
        return super().destroy(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"user": self.request.user, "organizer_pk": self.kwargs["organizer_pk"]}


class ListEvenImageApiView(GenericAPIView):
    """List all Event Images"""

    serializer_class = EventImageSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return EventImage.objects.all()

        return EventImage.objects.filter(Q(event__organizer__user_id=user.id) | Q(event__is_private=False))

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)

        data = {
            "status": "Success",
            "message": "Event image retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class EventImageApiView(GenericAPIView):
    '''Get and create a new picture for the events with a given pk. 
    Admin and organizer can add image and have access to this endpoint, others can only see public event images.'''

    serializer_class = EventImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        event_pk = self.kwargs['event_pk']

        event_images = EventImage.objects.filter(event_id=event_pk)
        first_event_image = event_images.first()

        if not first_event_image:
            return EventImage.objects.none()

        event = first_event_image.event
        if user.is_staff or event.organizer.user == user:
            return event_images

        if event.is_private:
            raise PermissionDenied(
                'You have no permissions to view this image')
        return event_images

    def get(self, request, *args, **kwargs):
        event_images = self.get_queryset()
        serializer = self.get_serializer(event_images, many=True)

        data = {
            "status": "Success",
            "message": "Images attached to the event with the given id retrieved.",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "status": "Success",
            "message": "New Event image added successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {"user": self.request.user, "event_pk": self.kwargs["event_pk"]}


class EventImageDetailApiView(RetrieveUpdateDestroyAPIView):
    ''' Retrieves Event image by ID for edit.'''

    serializer_class = EventImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        image_id = self.kwargs['pk']
        event_image = get_object_or_404(EventImage, id=image_id)

        # Allow access if the user is a staff member
        if user.is_staff:
            return event_image

        # Only allow the organizer of the event to access the image
        if event_image.event.organizer.user != user:
            raise PermissionDenied(
                'You do not have permission to access this image.')
        return event_image

    def destroy(self, request, *args, **kwargs):
        '''Check it the person trying to delete an image is the event organizer or staff, 
        cause they are the only one who should be able to.'''

        event_image = self.get_object()
        serializer = self.get_serializer(event_image)

        event_pk = self.kwargs['event_pk']
        serializer.validate_event_owner(event_id=event_pk)

        return super().destroy(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"user": self.request.user, "event_pk": self.kwargs["event_pk"]}
