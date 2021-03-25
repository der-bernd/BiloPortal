from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ResponsibleCreationForm, ResponsibleChangeForm
from .models import Responsible


class ResponsibleAdmin(UserAdmin):
    add_form = ResponsibleCreationForm
    form = ResponsibleChangeForm
    model = Responsible
    list_display = ('mail', 'company', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'company')
    fieldsets = (
        (None, {'fields': ('mail', 'first_name',
                           'last_name', 'company', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mail', 'first_name', 'last_name', 'company', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('mail',)
    ordering = ('mail',)


admin.site.register(Responsible, ResponsibleAdmin)
