from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent =  models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    
    def __str__(self):
        return self.name
    
    def is_main_category(self):
        return self.parent is None


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    subcategory = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.product.name
