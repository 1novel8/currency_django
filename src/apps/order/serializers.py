from rest_framework import serializers

from apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'type',
            'price',
            'finished_at',
            'status',
            'wallet',
        )
        read_only_fields = (
            'id',
            'finished_at',
            'status',
        )
