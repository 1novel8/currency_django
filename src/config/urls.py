from django.contrib import admin
from django.urls import include, path

api = [
    path('', include('apps.authentication.urls')),
    path('', include('apps.currency.urls')),
]

urlpatterns = [
    path('api/', include(api)),
    path('admin/', admin.site.urls),
]
