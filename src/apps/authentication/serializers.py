from typing import Any

from rest_framework import serializers

from apps.authentication.exceptions import NewPasswordCannotBeOld


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


class ChangePasswordSerializer(serializers.Serializer):
    """ Serializer for password """

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password1 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict[str, Any]) -> Any:
        """ Check if new passwords the same and new isn't old """

        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password1 = attrs.pop('new_password1')
        if new_password != new_password1:
            raise serializers.ValidationError("New passwords do not match.")
        if new_password == old_password:
            raise NewPasswordCannotBeOld

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset.
    User should know email and password.
    """

    username = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)
