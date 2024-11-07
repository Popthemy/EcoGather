from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=30, write_only=True)
    confirm_password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                "Password and Confirm_password doesn't match")

        validate_password(password)

        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = User.objects.create_user(
            email=email,
            password=password,
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    return attrs
                raise serializers.ValidationError('Invalid Password!')
            raise serializers.ValidationError('Invalid Email!')
        raise serializers.ValidationError('Email or Password are required!')
