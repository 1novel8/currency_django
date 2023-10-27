from rest_framework import serializers

from apps.user.models import Wallet


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
