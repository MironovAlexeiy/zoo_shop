
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('', include('main.urls')),
    path('api/v1/', include('zoo_api.urls')),
    path('api/v1/drf-auth', include('rest_framework.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
