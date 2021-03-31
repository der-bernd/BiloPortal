from django.contrib import admin
from .models import *
from .admin_filters import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = [HasMotherCompanyFilter]
    list_display = ['name', 'city', 'details', 'mother_company']


# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site
class ArticleInline(admin.TabularInline):
    model = Equipment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['name', 'price', 'duration', 'notes']
    inlines = [ArticleInline]


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
    list_filter = ['group']
    list_display = ['name', 'get_price', 'duration']

    def get_price(self, obj):  # https://realpython.com/customize-django-admin-python/
        return str(obj.price) + ' €'


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['article', 'service', 'amount']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['name', 'support_mail', 'products']

    def products(self, obj):
        return Article.objects.filter(manufacturer=obj).count()

    # def queryset(self, request): # see: https://stackoverflow.com/questions/2168475/django-admin-how-to-sort-by-one-of-the-custom-list-display-fields-that-has-no-d
    #     qs = super(ManufacturerAdmin, self).get_queryset(request)
    #     qs = qs.annotate(models.Count('article'))
    #     return qs

    # def number_of_products(self, obj):
    #     return obj.article__count
    # number_of_products.admin_order_field = 'number_of_products'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['com_name', 'ser_name', 'amount', 'assigned_employee',
                    'created', 'updated', 'start_date', 'end_date']


""" @admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
 """


admin.site.site_header = 'Bilobit Portal Administration'
