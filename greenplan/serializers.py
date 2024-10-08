from rest_framework import serializers
from greenplan.models import Event, Program, Organizer, Address
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


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
    program = ProgramSerializer()

    class Meta:
        model = Event
        fields = ['id', 'code', 'title', 'slug', 'organizer', 'description', 'program','is_private',
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
