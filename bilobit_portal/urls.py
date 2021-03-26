from django.contrib import admin
from django.urls import path, include

from .views import test

urlpatterns = [
    path('', include('info_pages.urls')),

    path('test/', test, name="test"),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls')),
]
