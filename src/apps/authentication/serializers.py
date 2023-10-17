from typing import Any

from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """ Serializer for registration """

    username = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=200, write_only=True)
    password1 = serializers.CharField(required=True, max_length=200, write_only=True)

    def validate(self, attrs: dict[str, Any]) -> Any:
        """ Check if passwords the same and creates only "password" field """

        password = attrs.get('password')
        password1 = attrs.pop('password1')
        if password != password1:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs


class LoginSerializer(serializers.Serializer):
    """Login Serializer"""

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, max_length=200, write_only=True)
