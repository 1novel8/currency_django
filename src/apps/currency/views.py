from django.conf import settings
from kafka import KafkaProducer
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.base.mixins import PermissionsByActionMixin, SerializeByActionMixin
from apps.currency.models import Currency
from apps.currency.serializers import CurrencySerializer, CurrencySubscribeSerializer, CurrencyUnsubscribeSerializer
from apps.currency.services import CurrencyService


class CurrencyViewSet(
    SerializeByActionMixin,
    PermissionsByActionMixin,
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
):
    """ ViewSet for Currency """

    permissions_by_action = {
        'create': [permissions.IsAdminUser],
        'retrieve': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAdminUser],
        'partial_update': [permissions.IsAdminUser],
        'list': [permissions.IsAuthenticated],
        'update': [permissions.IsAdminUser],
        'subscribe': [permissions.IsAuthenticated],
        'unsubscribe': [permissions.IsAuthenticated],
    }
    serialize_by_action = {
        'subscribe': CurrencySubscribeSerializer,
        'unsubscribe': CurrencyUnsubscribeSerializer,
    }
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    service = CurrencyService()

    @action(detail=True, methods=['post'])
    def subscribe(self, request: Request, pk: str) -> Response:
        self.service.subscribe(user=request.user, currency_pk=int(pk))
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request: Request, pk: str) -> Response:
        self.service.unsubscribe(user=request.user, currency_pk=int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer: CurrencySerializer) -> None:
        super().perform_create(serializer)
        producer = KafkaProducer(bootstrap_servers=settings.KAFKA_URL)
        producer.send('new_currencies', value=serializer.validated_data['name'].encode('utf-8'))
        producer.flush()
