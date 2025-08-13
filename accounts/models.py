from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import phonenumbers
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def clean(self):
        if self.phone_number:
            try:
                parsed = phonenumbers.parse(self.phone_number, None)
                if not phonenumbers.is_valid_number(parsed):
                    raise ValidationError("Número de teléfono inválido")
            except phonenumbers.phonenumberutil.NumberParseException:
                raise ValidationError("Formato de teléfono incorrecto")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()