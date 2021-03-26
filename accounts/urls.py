from django.urls import path
from .views import responsible_create_update, responsible_delete
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('<uuid:com_id>/add-responsible/',
         responsible_create_update, name='add-responsible'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/change_password.html',
            success_url='/'
        ),
        name='change-password'
    ),
    path('delete-responsible/<uuid:resp_id>/',
         responsible_delete, name='delete-responsible'),
]
