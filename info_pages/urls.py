from django.contrib import admin
from django.urls import path, include

from .views import home_view, about_view, redirect_to_home

app_name = 'info_pages'

urlpatterns = [
    path('', redirect_to_home),

    path('home/', home_view, name="home"),
    path('about/', about_view, name="about"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
