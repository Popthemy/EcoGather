from rest_framework import serializers
from greenplan.models import Event, Program
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count

CustomUser = get_user_model()


class BasicProgramSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Program
        fields = ['id', 'title']


class BasicCustomUser(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name']


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    organizer = BasicCustomUser()
    event_status = serializers.SerializerMethodField()
    organizer_events_count = serializers.SerializerMethodField()
    program = BasicProgramSerializer()

    class Meta:
        model = Event
        fields = ['id', 'code', 'title', 'slug', 'organizer', 'description', 'program',
                  'location', 'event_status', 'organizer_events_count', 'start_datetime', 'end_datetime', 'contact_email', 'contact_phone_number']

    def get_organizer_events_count(self, event):
        return event.get_organizer_total_events()

    def get_event_status(self, event):
        return event.get_event_status()


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['code', 'title', 'slug', 'description', 'program',
                  'location','start_datetime', 'end_datetime', 'contact_email', 'contact_phone_number']
