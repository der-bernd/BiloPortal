from django.contrib.admin import SimpleListFilter
from .models import Company

# src: https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter


class HasMotherCompanyFilter(SimpleListFilter):
    title = 'having a mother company'

    parameter_name = 'mother_company'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No')
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(mother_company__isnull=True)
        elif self.value() == 'no':
            return queryset.exclude(mother_company__isnull=False)


class ServiceDurationFilter(SimpleListFilter):
    title = 'having a mother company'

    parameter_name = 'mother_company'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No')
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(mother_company__isnull=True)
        elif self.value() == 'no':
            return queryset.exclude(mother_company__isnull=False)
