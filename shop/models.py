from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from django.urls import reverse

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text="Nombre publico de tu tienda")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    logo = models.ImageField(upload_to='shop_logos/')
    description = models.CharField(max_length=255, help_text="Describe your products (min. 20 characters).")
    category = models.ForeignKey('ecommerce.Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoria Principal')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    terms_accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default="pending", choices=[("active", "Active"), ("pending", "Pending"), ("suspended", "Suspended")])
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.owner.username}"
    
    @property
    def has_half_rating(self):
        return self.average_rating % 1 >= 0.5
    
    def get_absolute_url(self):
        return reverse('store_front', kwargs={'store_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        counter = 1
        while Shop.objects.filter(slug=self.slug).exists():
            self.slug = f"{slugify(self.name)}-{counter}"
            counter += 1
        
        if not self.pk:
            if self.terms_accepted and self.logo:
                self.status = 'active'
            #TODO: Notify admins for new flows.
        super().save(*args, **kwargs)


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
