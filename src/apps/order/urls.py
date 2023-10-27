from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.order.views import OrderViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]
