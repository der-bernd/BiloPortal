from django.urls import path
from .views import import_articles, app_overview
from django.contrib.auth import views as auth_views

app_name = 'frontend_admin'

urlpatterns = [
    path('',
         app_overview, name='home'),
    path('import/',
         import_articles, name='import'),
]
