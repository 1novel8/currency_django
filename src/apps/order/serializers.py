from typing import Any

from rest_framework import serializers

from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'type',
            'price',
            'count',
            'finished_at',
            'status',
            'wallet',
        )
        read_only_fields = (
            'id',
            'finished_at',
            'status',
        )

    def validate(self, attrs: dict[str, Any]) -> Any:
        """
        Check if price field is not None.
        """

        if attrs['price'] is None:
            raise serializers.ValidationError("Price should be filled")
        return attrs


class QuickOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'type',
            'count',
            'finished_at',
            'status',
            'wallet',
        )
        read_only_fields = (
            'id',
            'finished_at',
            'status',
        )

    def validate(self, attrs: dict[str, Any]) -> Any:
        """
        Add price field as None.
        It means that user don't care what price now.
        """

        attrs['price'] = None
        return attrs


class OrderCancelSerializer(serializers.Serializer):
    pass
