from rest_framework import serializers
from greenplan.models import Event, Program
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
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
                  'venue','city_or_state', 'event_status', 'organizer_events_count', 'start_datetime', 'end_datetime', 'contact_email', 'contact_phone_number']

    def get_organizer_events_count(self, event):
        return event.get_organizer_total_events()

    def get_event_status(self, event):
        return event.get_event_status()


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['code', 'title', 'slug', 'description', 'program',
                  'venue','city_or_state', 'start_datetime', 'end_datetime', 'contact_email', 'contact_phone_number']

        def validate(self, attrs):
            '''Validate details from users'''

            errors = {}

            if not attrs.get('code'):
                errors['code'] = [
                    'Input a unique code for this event e.g SDG2025']
            if not attrs.get('title'):
                errors['title'] = ['Title is required']
            if not attrs.get('program'):
                errors['program'] = [
                    'Program is required. Enter the type of program your event belongs to e.g Seminar, Conference..']
            if not attrs.get('location'):
                errors['location'] = ['Location is required']
            if not attrs.get('start_datetime'):
                errors['start_datetime'] = ['start_datetime is required']
            if not attrs.get('end_datetime'):
                errors['end_datetime'] = ['end_datetime is required']

            if errors:
                raise serializers.ValidationError(errors)
            return attrs

        # def create(self, validated_data):
        #     user = self.context['user']
        #     program = validated_data['program']

        #     if program and user:
        #         program, created = Program.objects.get_or_create(
        #             title=(program).capitalize())

        #         return Event.objects.create(organizer=user, **validated_data)
        #     raise serializers.ValidationError("Event not created")


        def create(self, validated_data):
            # Ensure user is correctly retrieved from context
            user = self.context['organizer']
            if not user:
                raise serializers.ValidationError(
                    "User is not authenticated or not provided in context.")

            # Ensure required fields are present
            if 'program' in validated_data:
                program = validated_data['program']
                program, created = Program.objects.get_or_create(
                    title=program.capitalize())
            else:
                raise serializers.ValidationError("Program is required.")

            # Create and return the event with the user as organizer
            return Event.objects.create(organizer=user, **validated_data)
        
