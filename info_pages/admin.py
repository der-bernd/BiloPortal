from django.contrib import admin

from .models import FAQ
from .admin_filters import HasRelatedServiceFilter

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_filter = [HasRelatedServiceFilter]
    list_display = ['question', 'answer', 'service']
