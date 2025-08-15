from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at')
    list_editable = ('status',)  # Allow bulk status updates
    actions = ['approve_shops']

    def approve_shops(self, request, queryset):
        queryset.update(status='active')
    approve_shops.short_description = "Approve selected shops"
