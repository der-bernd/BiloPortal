from django.urls import path
from .views import import_articles
from django.contrib.auth import views as auth_views

app_name = 'frontend_admin'

urlpatterns = [
    path('import-articles/',
         import_articles, name='import-articles'),
]
