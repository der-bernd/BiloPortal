from django.urls import path
from .views import responsible_create_update

app_name = 'accounts'

urlpatterns = [
    path('<uuid:com_id>/add-responsible/',
         responsible_create_update, name='signup'),
]
