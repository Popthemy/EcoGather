from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from greenplan.models import Event
from greenplan.serializers import EventSerializer, CreateEventSerializer

# Create your views here.


class EventApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

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
            return qs.filter(organizer=user)

        # If no events found or user isn't authenticated
        return qs.none()

    def get(self, request, *args, **kwargs):
        events = self.get_queryset()
        total_events = events.count()

        serializer = self.get_serializer(events, many=True)
        data = {
            "status": "success",
            "message": "Events retrieved successfully",
            'total_events': total_events,
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer = serializer(data=request.data)
        return super().post(request, *args, **kwargs)

    def get_serializer_context(self):
        return {'request': self.request}
