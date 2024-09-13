from rest_framework import serializers
from greenplan.models import Event


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ['id','code','title','slug','organizer','location','start','end']
