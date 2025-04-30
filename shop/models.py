from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='shop_logos/')
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.name + ' - ' + self.owner.username

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=255)
    #TODO Add email support for User and Customer model.
    # email = models.EmailField(unique=True)
    phone = models.TextField()
    address = models.TextField()
    last_updated = models.DateTimeField(auto_now_add=True)

