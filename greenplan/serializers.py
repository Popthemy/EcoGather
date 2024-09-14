from rest_framework import serializers
from greenplan.models import Event
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class BasicCustomUser(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name']


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    organizer = BasicCustomUser()

    class Meta:
        model = Event
        fields = ['id', 'code', 'title', 'slug', 'organizer',
                  'location', 'start_datetime', 'end_datetime']
