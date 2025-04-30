from django.contrib import admin
from .models import Product, Review, Category

class ProductAdmin(admin.ModelAdmin):
    ordering = ['name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Category)