from rest_framework import serializers

from apps.currency.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Currency
        fields = [
            'id',
            'image',
            'name',
            'price_for_buy',
            'price_for_sale',
        ]


class CurrencySubscribeSerializer(serializers.Serializer):
    pass


class CurrencyUnsubscribeSerializer(serializers.Serializer):
    pass
