from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomerSupportTicket(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='cs_tickets/')
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_number = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            last_ticket = CustomerSupportTicket.objects.order_by('-id').first()
            if last_ticket and last_ticket.ticket_number:
                # Extract number part
                try:
                    last_number = int(last_ticket.ticket_number.split('-')[1])
                except (IndexError, ValueError):
                    last_number = 0
            else:
                last_number = 0

            self.ticket_number = f"IST-{last_number + 1}"

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.ticket_number}: {self.title}"
