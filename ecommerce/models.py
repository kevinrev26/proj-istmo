from django.db import models
from django.contrib.auth.models import User
from shop.models import Shop
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

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
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        from django.db.models import Avg
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    @property
    def has_half_rating(self):
        """Check if rating has 0.5 fraction"""
        return self.average_rating % 1 >= 0.5 if self.average_rating else False
    
    @property
    def full_stars(self):
        """Number of full stars to display"""
        return int(self.average_rating) if self.average_rating else 0
    
    @property
    def display_rating(self):
        """Generate HTML for star rating display"""
        rating = self.average_rating
        full_stars = int(rating)
        half_star = rating % 1 >= 0.5
        empty_stars = 5 - full_stars - (1 if half_star else 0)
        
        stars = []
        stars.extend(['<i class="fas fa-star"></i>'] * full_stars)
        if half_star:
            stars.append('<i class="fas fa-star-half-alt"></i>')
        stars.extend(['<i class="far fa-star"></i>'] * empty_stars)
        
        return mark_safe(''.join(stars))
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.product.name

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now_add=True)
    
class StockMovement(models.Model):
    MOVEMENT_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=8, choices=MOVEMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
