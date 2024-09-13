from django.shortcuts import render
from rest_framework.views import APIView
from greenplan.models import Event
from rest_framework.response import Response
from rest_framework import status

from greenplan.serializers import EventSerializer

# Create your views here.


class EventView(APIView):
    serializer_class = EventSerializer

    def get(self, request):
        events = Event.objects.all()
        serializer = self.serializer_class(events, many=True)

        data = {
            "status": "success",
            "message": "Event retrieved successfully",
            "data": serializer.data 
        }

        return Response(data,status=status.HTTP_200_OK)
        # return Response({
        #       "status": "Error",
        #         "message": "Event retrieved unsuccessfully",
        #         "errors": serializer.errors
            
        # }, status=status.HTTP_400_BAD_REQUEST)
    

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
        
        
    

