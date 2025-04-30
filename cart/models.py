from django.db import models
from django.contrib.auth.models import User
from ecommerce.models import Product
from shop.models import Shop

class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        PENDING = 1
        IN_PROCESS = 2
        DISPATCHED = 3
        DONE = 4
        CANCELED = 5

    id  = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    status = models.IntegerField(choices=OrderStatus, default=OrderStatus.PENDING)

    def __str__(self):
        return str(self.id) + ' - ' + self.user.username
    
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.product.name