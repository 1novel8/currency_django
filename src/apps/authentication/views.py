from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.authentication.serializers import LoginSerializer, RegisterSerializer
from apps.authentication.services import AuthenticationService
from apps.base.mixins import SerializeByActionMixin
from apps.user.models import User


class AuthenticationViewSet(
    SerializeByActionMixin,
    GenericViewSet,
):
    """ Auth ViewSet """

    serialize_by_action = {
        'register': RegisterSerializer,
        'login': LoginSerializer,
    }
    permission_classes = [permissions.AllowAny]
    service = AuthenticationService()
    queryset = User.objects.all()

    @action(detail=False, methods=['post'])
    def login(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jwt = self.service.generate_jwt(**serializer.validated_data)
        return Response(data={'token': jwt}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def register(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.service.create_user(**serializer.validated_data)
        serializer = self.get_serializer(user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
