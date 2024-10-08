from rest_framework import serializers
from greenplan.models import Event, Program, Organizer, Address
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html,urlencode


CustomUser = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    """{
    "street_number": 5,
    "street_name": "Stadium",
    "city": "Ogbomosho",
    "state": "Oyo",
    "zip_code": null,
    "country": "Nigeria"
    }"""

    id = serializers.IntegerField(read_only=True)
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'organizer', 'street_number', 'street_name',
                  'city', 'state', 'zip_code', 'country']

    def create(self, validated_data):
        organizer = self.context['request'].user
        return Address.objects.create(organizer_id=organizer.pk, **validated_data)


class OrganizerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, source='user_id')
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Organizer
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'type', 'phone_number', 'bio', 'vision', 'mission', 'addresses']

    def create(self, validated_data):
        user = self.context['request'].user
        user_instance = get_object_or_404(CustomUser, pk=user.id)

        return Organizer.objects.create(user=user_instance, **validated_data)


class MiniOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['username', 'type']


class MiniEventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    event_status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'event_status',
                  'venue']

    def get_event_status(self, event):
        return event.get_event_status()


class ProgramSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    featured_event = MiniEventSerializer(read_only=True)
    featured_event_id = serializers.IntegerField(write_only=True)
    events = MiniEventSerializer(many=True, read_only=True)
    program_event_count = serializers.SerializerMethodField()
    program_url = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ['id', 'title', 'program_event_count','program_url',
                  'featured_event', 'featured_event_id', 'events']


    def validate_featured_event_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'featured event id must be greater the 0 e.g 1,2,3')
        return value


    def get_program_url(self,program):
        '''get a link that leads to a program list of events.'''

        request = self.context['request']
        url = reverse('programs-detail',kwargs={'pk':program.id})
        full_path = request.build_absolute_uri(url)
        return full_path


    def get_program_event_count(self, program):
        '''get a link that leads to a program list of events in that program.'''
        return program.events.count()


    def create(self, validated_data):
        ''' Create a program we want to create based on the required field(title) first, 
        then check if the featured-d is present and then add '''

        featured_event_id = validated_data.pop('featured_event_id', None)
        program = Program.objects.create(**validated_data)
        if featured_event_id is not None:
            program.featured_event_id = featured_event_id
            program.save()
        return program


    def update(self, instance, validated_data):
        featured_event_id = validated_data.pop('featured_event_id', None)
        instance = super().update(instance, validated_data)

        if featured_event_id is not None:
            instance.featured_event_id = featured_event_id
            instance.save()

        return instance  



class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    organizer = MiniOrganizerSerializer()
    organizer_url = serializers.HyperlinkedRelatedField(
        queryset=Organizer.objects.all(),
        view_name='organizers-detail', source='organizer'
    )
    event_status = serializers.SerializerMethodField()
    organizer_events_count = serializers.SerializerMethodField()
    program = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = ['id', 'code', 'title', 'slug', 'organizer', 'organizer_url', 'description', 'program', 'is_private',
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

        if program and user:
            program, created = Program.objects.get_or_create(
                title=str(program).capitalize())

            organizer = get_object_or_404(Organizer, email=user.email)
            event = Event.objects.create(
                organizer=organizer, **validated_data)

            return event

        raise serializers.ValidationError('user or program are required')
