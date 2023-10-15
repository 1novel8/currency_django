from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.authentication.views import AuthenticationViewSet

router = DefaultRouter()
router.register('auth', AuthenticationViewSet, basename='auth')


urlpatterns = [
    path('', include(router.urls)),
]
