from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('info_pages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls')),
]
