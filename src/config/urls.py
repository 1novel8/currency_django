from django.contrib import admin
from django.urls import include, path

api = [
    path('', include('apps.authentication.urls')),
    path('', include('apps.currency.urls')),
    path('', include('apps.user.urls')),
    path('', include('apps.order.urls'))
]

urlpatterns = [
    path('api/', include(api)),
    path('admin/', admin.site.urls),
]
