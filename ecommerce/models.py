from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')


    def __str__(self):
        return str(self.id) + ' - ' + self.name