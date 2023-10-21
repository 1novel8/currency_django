from rest_framework import serializers

from apps.currency.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            'id',
            'name',
            'price_for_buy',
            'price_for_sale',
        ]


class CurrencySubscribeSerializer(serializers.Serializer):
    pass


class CurrencyUnsubscribeSerializer(serializers.Serializer):
    pass
