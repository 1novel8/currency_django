from rest_framework import serializers

from apps.user.models import User, Wallet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'role',
            'balance',
        )


class TopUpBalanceSerializer(serializers.Serializer):
    count = serializers.DecimalField(
        max_digits=16,
        decimal_places=6,
    )


class ChangeRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('role', )


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'id',
            'currency',
            'balance',
        ]
        read_only_fields = (
            'id',
            'balance',
            'user_id',
        )
