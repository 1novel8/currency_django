from typing import Any

from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """ Serializer for registration """

    username = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, max_length=200, write_only=True)
    password2 = serializers.CharField(required=True, max_length=200, write_only=True)

    def validate(self, attrs: dict[str, Any]) -> Any:
        password1 = attrs.pop('password1')
        password2 = attrs.pop('password2')
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        attrs['password'] = password1
        return attrs
