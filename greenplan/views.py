from django.shortcuts import render
from django.http import Http404
from django.db.models.aggregates import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from greenplan.models import Event
from greenplan.serializers import EventSerializer

# Create your views here.


class EventApiView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        qs = Event.objects.select_related('organizer','program')

        # Admin sees all the events
        if user.is_staff:
            return qs

        # Regular authenticated users see only their events
        if user.is_authenticated:
            return qs.filter(organizer=user)

        # If no events found or user isn't authenticated
        return qs.none()

    def get(self, request):
        events = self.get_object()
        total_events = events.count()
        if events:
            serializer = self.serializer_class(events, many=True)

            data = {
                "status": "success",
                "message": "Event retrieved successfully",
                'total event': total_events,
                "data": serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)
        return Response({
            "status": "Error",
            "message": "Event retrieved unsuccessfully",
            "errors": "You have no event yet!"

        }, status=status.HTTP_400_BAD_REQUEST)

    # def post(self,request,*args, **kwargs):

    #     title = self.request.get('title','')
    #     slug = self.request.get('slug','')
    #     start = self.request.get('start_time','')
    #     "code": "FINA2025",
    #         "title": "Pan-African Financial Summit",
    #         "slug": null,
    #         "organizer": "f55d0335-2c63-4a94-988f-2d1735d8d766",
    #         "location": "Johannesburg, South Africa",
    #         "start_time": "2024-10-13T12:59:20.312334Z",
    #         "end_time": "2024-10-18T12:59:20.312334Z"
    #     },
