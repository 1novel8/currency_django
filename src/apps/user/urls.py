from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.user.views import UserViewSet, WalletViewSet

router = DefaultRouter()
router.register('wallets', WalletViewSet, basename='wallet')
router.register('users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
]
