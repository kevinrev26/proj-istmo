from django.contrib import admin
from django.utils.html import format_html
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at', 'store_link')
    readonly_fields = ('store_link',)
    list_editable = ('status',)  # Allow bulk status updates
    actions = ['approve_shops']

    def approve_shops(self, request, queryset):
        queryset.update(status='active')
    approve_shops.short_description = "Approve selected shops"

    def store_link(self, obj):
        return format_html('<a href="{0}" target="_blank">{0}</a>', obj.get_absolute_url())
    store_link.short_description = 'Store URL'