from rest_framework import serializers
from greenplan.models import Event, Program, Organizer, Address
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404


CustomUser = get_user_model()


class OrganizerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=32,read_only=True, source='user_id')

    class Meta:
        model = Organizer
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'type', 'phone_number', 'bio', 'vision', 'mission']
        
    
    def create(self, validated_data):
        user = self.context['request'].user
        user_instance = get_object_or_404(CustomUser,pk=user.id)
        
        return Organizer.objects.create(user=user_instance, **validated_data)

class ProgramSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Program
        fields = ['id', 'title', 'featured_event']


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    organizer = serializers.HyperlinkedRelatedField(
        queryset=Organizer.objects.all(),
        view_name='organizer_details'
    )
    event_status = serializers.SerializerMethodField()
    organizer_events_count = serializers.SerializerMethodField()
    program = ProgramSerializer(required=True)

    class Meta:
        model = Event
        fields = ['id', 'code', 'title', 'slug', 'organizer', 'description', 'program',
                  'venue', 'city_or_state', 'event_status', 'organizer_events_count', 'start_datetime', 'end_datetime', 'contact_email', 'contact_phone_number']

    def get_organizer_events_count(self, event):
        return event.get_organizer_total_events()

    def get_event_status(self, event):

        return event.get_event_status()


class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['code', 'title', 'slug', 'description', 'program',
                  'venue', 'city_or_state', 'start_datetime', 'end_datetime', 'contact_email', 'contact_phone_number']

    def create(self, validated_data):
        user = self.context['request'].user

        program = validated_data['program']
        print(f'user: {user} program:{program}')

        if program and user:
            program, created = Program.objects.get_or_create(
                title=str(program).capitalize())

            organizer = get_object_or_404(Organizer, email=user.email)
            event = Event.objects.create(
                organizer=organizer, **validated_data)

            return event

        raise serializers.ValidationError('user or program are required')
