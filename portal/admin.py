from django.contrib import admin
from .models import *
from .admin_filters import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = [HasMotherCompanyFilter]
    list_display = ['name', 'city', 'details']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['name', 'price', 'duration', 'notes']


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['name', 'mother_group']


@admin.register(ArticleGroup)
class GroupAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['name', 'mother_group']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'mail', 'company']
    list_filter = []


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['name', 'description', 'price', 'duration']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['article', 'service', 'amount']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['name', 'support_mail', 'notes']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['com_name', 'ser_name', 'amount',
                    'created', 'updated', 'start_date', 'end_date']


""" @admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
 """


admin.site.site_header = 'Bilobit Portal Administration'
