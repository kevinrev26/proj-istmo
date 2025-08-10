from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='shop_logos/')
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #TODO: Add creation time

    def __str__(self):
        return str(self.id) + ' - ' + self.name + ' - ' + self.owner.username


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    features = models.TextField(help_text="One feature per line")
    
    class Meta:
        verbose_name = "Plan de Suscripción"
        verbose_name_plural = "Planes de Suscripción"
    
    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    is_trial = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    next_billing_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    
    @property
    def days_remaining(self):
        return (self.end_date - datetime.now()).days