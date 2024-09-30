from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from greenplan.models import Event,Organizer
from greenplan.serializers import ListEventSerializer, CreateEventSerializer,OrganizerSerializer
from uuid import UUID
# Create your views here.

@api_view(['GET'])
def list_events(request):
    events  = Event.objects.select_related('program','organizer').all()
    serializer = ListEventSerializer(events,many=True,context= {'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def organizer_detail(request,pk):
    organizer = get_object_or_404(Organizer,pk=pk)
    serializer = OrganizerSerializer(organizer)
    return Response(serializer.data)

class EventApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateEventSerializer
        else:
            return ListEventSerializer
    
    def get_serializer(self, *args, **kwargs):

        serializer_class =  self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['context']['organizer'] = self.request.user

        return serializer_class(*args, **kwargs)

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            serializer = EventSerializer(serializer)
            data = {
                "status":"success",
                "message": " Event Created successfully",
                "data":serializer.data
            }

            return Response(data,status=status.HTTP_201_CREATED)
        error_message = {'status':'failed',
                         'message':'Event not created'}
        return Response(error_message,status=status.HTTP_400_BAD_REQUEST)
    

    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         event = self.perform_create(serializer)
    #         serializer  = EventSerializer(event)
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        return {'request': self.request,'user': self.request.user}
