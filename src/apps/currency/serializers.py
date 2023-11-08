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


class CurrencyUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=True)
    price_for_buy = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    price_for_sale = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)


class CurrencySubscribeSerializer(serializers.Serializer):
    pass


class CurrencyUnsubscribeSerializer(serializers.Serializer):
    pass
