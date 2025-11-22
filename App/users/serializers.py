"""Serializers for the User API.

Reformatted for PEP 8 and added clear docstrings.
No business logic has been changed.
"""

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    """Serializer for creating and updating users."""

    password = serializers.CharField(
        write_only=True,
        min_length=5,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        """Create and return a new user with encrypted password."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly if provided."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for authenticating users and generating tokens."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate user credentials."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate using the provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs