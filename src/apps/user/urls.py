from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.user.views import WalletViewSet

router = DefaultRouter()
router.register('wallets', WalletViewSet, basename='wallet')


urlpatterns = [
    path('', include(router.urls)),
]
