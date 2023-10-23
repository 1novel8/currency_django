from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.currency.views import CurrencyViewSet

router = DefaultRouter()
router.register('currencies', CurrencyViewSet, basename='currency')


urlpatterns = [
    path('', include(router.urls)),
]
