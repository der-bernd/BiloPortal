from django.contrib.admin import SimpleListFilter
from .models import FAQ

# src: https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter


class HasRelatedServiceFilter(SimpleListFilter):
    title = 'having a related service'

    parameter_name = 'service'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No')
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(service__isnull=True)
        elif self.value() == 'no':
            return queryset.exclude(service__isnull=False)

