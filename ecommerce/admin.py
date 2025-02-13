from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    ordering = ['name']

admin.site.register(Product, ProductAdmin)