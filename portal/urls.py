from django.urls import path, include
from django.contrib import admin

# easy deployment, but security risk, should be removed in production!
from .views import *
# from accounts.views import signup_view

app_name = "portal"

urlpatterns = [
    path('', app_overview, name="overview"),

    # company stuff
    path('company/', company_detail, name="my-detail"),
    path('company-list/', company_list_view, name="company-list"),
    path('company/create/', company_create_update, name="create"),
    path('company/<uuid:com_id>/', company_detail, name="portal_company_detail"),
    path('company/<uuid:com_id>/delete/', company_delete, name="delete"),
    path('company/<uuid:com_id>/update/', company_create_update, name="update"),
    path('company/<uuid:com_id>/add-employee/',
         employee_create_update, name="add-employee"),
    path('company/<uuid:com_id>/update-employee/<uuid:em_id>/',
         employee_create_update, name="update-employee"),
    path('company/<uuid:com_id>/delete-employee/<uuid:em_id>/',
         employee_delete, name="delete-employee"),

    path('company/<uuid:com_id>/store/',
         service_store, name="service-store"),
    path('company/<uuid:com_id>/store/<uuid:service_id>/config/',
         service_config, name="service-config"),

    path('company/lengthen-booking/<uuid:booking_id>/',
         booking_edit, name="edit-booking"),
]
