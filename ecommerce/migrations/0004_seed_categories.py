# Generated by Django 5.1.2 on 2025-04-30 20:10

from django.db import migrations

def seed_categories(apps, schema_editor):
    Category = apps.get_model('ecommerce', 'Category')

    # Principal Categories
    electronics = Category.objects.create(name="Electronics")
    fashion = Category.objects.create(name="Fashion")
    home = Category.objects.create(name="Home & Kitchen")
    sports = Category.objects.create(name="Sports & Outdoors")

    # Subcategories for Electronics
    Category.objects.create(name="Smartphones", parent=electronics)
    Category.objects.create(name="Laptops", parent=electronics)
    Category.objects.create(name="Cameras", parent=electronics)

    # Subcategories for Fashion
    Category.objects.create(name="Men's Clothing", parent=fashion)
    Category.objects.create(name="Women's Clothing", parent=fashion)
    Category.objects.create(name="Accessories", parent=fashion)

    # Subcategories for Home
    Category.objects.create(name="Furniture", parent=home)
    Category.objects.create(name="Kitchen Tools", parent=home)

    # Subcategories for Sports
    Category.objects.create(name="Fitness Equipment", parent=sports)
    Category.objects.create(name="Outdoor Gear", parent=sports)

def unseed_categories(apps, schema_editor):
    Category = apps.get_model('ecommerce', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_product_shop_category_product_subcategory_stock_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_code=unseed_categories),
    ]
