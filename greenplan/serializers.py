from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html

from rest_framework import serializers
from greenplan.models import Program, Organizer, Address, Event, Template, CustomField, OrganizerImage, EventImage


CustomUser = get_user_model()


class MiniOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['username', 'type']


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


class OrganizerImageSerializer(serializers.ModelSerializer):
    ''' Display organizer images '''

    id = serializers.IntegerField(read_only=True)
    organizer = MiniOrganizerSerializer(read_only=True)

    class Meta:
        model = OrganizerImage
        fields = ['id', 'organizer', 'priority', 'image_url']

    def validate_org_id(self, organizer_id):
        ''' Validate the user who is trying to add image,
        the person must be staff or the current logged in user. 
        Raise if the organizer id doesn't match the currently logged in user and is not a staff'''

        user = self.context['user']

        if not user.is_staff and user.id != organizer_id:
            raise serializers.ValidationError(
                'You are trying to add image for another Organizer, but you can only add image for yourself.')

    def create(self, validated_data):
        '''Create new image for organizer with the attached id.'''
        organizer_pk = self.context['organizer_pk']

        self.validate_org_id(organizer_id=organizer_pk)

        organizer = OrganizerImage()
        organizer.organizer_id = organizer_pk
        organizer.priority = validated_data.get(
            'priority') or OrganizerImage.priority.default
        organizer.image_url = validated_data.get(
            'image_url') or OrganizerImage.image_url.field.default
        organizer.save()
        return organizer

    def update(self, instance, validated_data):
        '''Only the organizer or staff can edit their image detail'''

        organizer_pk = self.context['organizer_pk']

        self.validate_org_id(organizer_id=organizer_pk)

        if 'image_url' in validated_data and validated_data['image_url'] is None:
            validated_data['image_url'] = instance.image_url

        return super().update(instance, validated_data)


class OrganizerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, source='user_id')
    addresses = AddressSerializer(many=True, read_only=True)
    organizer_events_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organizer
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'organizer_events_count',
                  'type', 'phone_number', 'bio', 'vision', 'mission', 'addresses']

    def create(self, validated_data):
        user = self.context['request'].user
        user_instance = get_object_or_404(CustomUser, pk=user.id)

        return Organizer.objects.create(user=user_instance, **validated_data)

    def get_organizer_events_count(self, organizer):
        return organizer.get_organizer_total_events()


class MiniEventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    event_status = serializers.SerializerMethodField()
    organizer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'event_status', 'organizer',
                  'venue', 'is_private']

    def get_event_status(self, event):
        return event.get_event_status()


class ProgramSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    featured_event = MiniEventSerializer(read_only=True)
    featured_event_id = serializers.IntegerField(
        write_only=True, required=False)
    events = MiniEventSerializer(many=True, read_only=True)
    program_event_count = serializers.SerializerMethodField()
    program_url = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ['id', 'title', 'program_event_count', 'program_url',
                  'featured_event', 'featured_event_id', 'events']

    def validate_featured_event_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'featured event id must be greater the 0 e.g 1,2,3')
        get_object_or_404(Event, pk=value)
        return value

    def get_program_event_count(self, program):
        return program.events.count()

    def get_program_url(self, program):
        '''url to a single program with the list of all its events.'''

        request = self.context['request']
        url = reverse('programs-detail', kwargs={'pk': program.id})
        return request.build_absolute_uri(url)

    def create(self, validated_data):
        ''' Create a program we want to create based on the required field(title) first,
        then check if the featured-d is present and then add '''

        featured_event_id = validated_data.pop('featured_event_id', None)
        program = Program.objects.create(**validated_data)

        if featured_event_id is None:
            self.check_featured_event_program_clashes(
                instance=program, event_id=featured_event_id)
            program.featured_event_id = featured_event_id
            program.save()
        return program

    def update(self, instance, validated_data):
        """ Updating the program might involve removing its linked event or linking event."""
        featured_event_id = validated_data.pop('featured_event_id', None)
        instance = super().update(instance, validated_data)

        if featured_event_id is not None:
            self.check_featured_event_program_clashes(
                instance=instance, event_id=featured_event_id)
            instance.featured_event_id = featured_event_id
            instance.save()

        return instance

    def check_featured_event_program_clashes(self, instance: Program, event_id):
        '''Handle if there is a conflict:
        An event from program Convention` shouldn't be made featured_event of program `Webinar`
        This automatically makes sure a featured event belong to the progra '''

        event = Event.objects.filter(pk=event_id).first()

        if event.program != instance.title:
            event.program_id = instance.id
            event.save()


class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['code', 'title', 'slug', 'description', 'program', 'is_private',
                  'venue', 'city', 'start_datetime', 'end_datetime', 'contact_email', 'contact_phone_number']

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


class MiniCustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = ['id', 'label', 'content']


class CustomFieldSerializer(serializers.ModelSerializer):
    '''Serializer for template custom fields'''

    class Meta:
        model = CustomField
        fields = ['id', 'template', 'label',
                  'content', 'start_time', 'end_time']

    def create(self, validated_data):
        user = self.context['user']
        template_pk = self.context['template_pk']

        event = get_object_or_404(Event, templates=template_pk)
        if not user.is_staff or event.organizer.user != user:
            raise serializers.ValidationError(
                'You are not allowed to add field to this template. NOT ORGANIZER')

        return CustomField.objects.create(template_id=template_pk, **validated_data)

    def update(self, instance, validated_data):
        user = self.context['user']
        template_pk = self.context['template_pk']

        event = get_object_or_404(Event, templates=template_pk)

        if not user.is_staff and event.organizer.user != user:
            raise serializers.ValidationError(
                'You are not allowed to add field to this template. NOT ORGANIZER')

        return super().update(instance, validated_data)


class TemplateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # event = MiniEventSerializer(read_only=True)
    custom_fields = CustomFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Template
        fields = ['id', 'code', 'title', 'event',
                  'custom_fields', 'slug', 'description']

    def check_user_and_event_return_event(self, user, event_pk):
        if event_pk <= 0:
            raise serializers.ValidationError(
                'Event id must be positive e.g 1,2,3')

        event = get_object_or_404(Event, pk=event_pk)
        if not user.is_staff:
            if event.organizer.user != user:
                raise serializers.ValidationError(
                    'You are not the organizer of this event ')
        return event

    def create(self, validated_data):
        '''Create a template with an event, we should make sure that the user is the
        organizer of the event before creation'''

        user = self.context['user']
        pk = self.context['event_pk']

        event = self.check_user_and_event_return_event(user=user, event_pk=pk)

        template = Template.objects.create(
            owner_id=event.organizer.user.id,
            event_id=pk,
            **validated_data
        )
        return template

    def update(self, instance, validated_data):

        user = self.context['user']
        pk = self.context['event_pk']
        event = self.check_user_and_event_return_event(user=user, event_pk=pk)

        return super().update(instance, validated_data)


class MiniTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'code', 'title', 'custom_fields']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model, including organizer and event status.
    an event is organizer by an organizer, an event has more than one template ,each template can have many fields"""

    id = serializers.IntegerField(read_only=True)
    organizer = MiniOrganizerSerializer()
    organizer_url = serializers.HyperlinkedRelatedField(
        queryset=Organizer.objects.all(),
        view_name='organizers-detail', source='organizer'
    )
    event_status = serializers.SerializerMethodField()
    program = serializers.StringRelatedField()
    templates = TemplateSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'code', 'title', 'slug', 'organizer', 'organizer_url', 'description', 'templates', 'program', 'is_private',
                  'venue', 'city', 'event_status', 'start_datetime', 'end_datetime', 'contact_email', 'contact_phone_number']

    def get_event_status(self, event):
        return event.get_event_status()



class EventImageSerializer(serializers.ModelSerializer):
    ''' Display event images '''

    id = serializers.IntegerField(read_only=True)
    event = MiniEventSerializer(read_only=True)

    class Meta:
        model = EventImage
        fields = ['id', 'event', 'priority', 'image_url']

    def validate_org_id(self, event_id):
        ''' Validate the user who is trying to add image,
        the person must be staff or the current logged in user. 
        Raise if the organizer id doesn't match the currently logged in user and is not a staff'''

        user = self.context['user']

        if not user.is_staff and user.id != event_id:
            raise serializers.ValidationError(
                'You are trying to add image for another Organizer, but you can only add image for yourself.')

    def create(self, validated_data):
        '''Create new image for organizer with the attached id.'''
        organizer_pk = self.context['organizer_pk']

        self.validate_org_id(organizer_id=organizer_pk)

        organizer = OrganizerImage()
        organizer.organizer_id = organizer_pk
        organizer.priority = validated_data.get(
            'priority') or OrganizerImage.priority.default
        organizer.image_url = validated_data.get(
            'image_url') or OrganizerImage.image_url.field.default
        organizer.save()
        return organizer

    def update(self, instance, validated_data):
        '''Only the organizer or staff can edit their image detail'''

        organizer_pk = self.context['organizer_pk']

        self.validate_org_id(organizer_id=organizer_pk)

        if 'image_url' in validated_data and validated_data['image_url'] is None:
            validated_data['image_url'] = instance.image_url

        return super().update(instance, validated_data)
