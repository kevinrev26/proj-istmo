from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import Subscription
from django.core.mail import send_mail
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = 'Checks for expiring subscriptions and sends notifications'
    
    def handle(self, *args, **options):
        # Get subscriptions expiring in 3 days
        warning_date = timezone.now() + timezone.timedelta(days=3)
        expiring = Subscription.objects.filter(
            end_date__lte=warning_date,
            is_active=True
        )
        
        for subscription in expiring:
            # Send email notification
            context = {
                'user': subscription.user,
                'plan': subscription.plan,
                'days_remaining': (subscription.end_date - timezone.now()).days
            }
            
            html_message = render_to_string('emails/trial_ending.html', context)
            text_message = render_to_string('emails/trial_ending.txt', context)
            
            send_mail(
                'Tu prueba gratuita está por terminar',
                text_message,
                'notificaciones@istmopay.com',
                [subscription.user.email],
                html_message=html_message,
                fail_silently=True
            )
            
            self.stdout.write(f"Sent notification to {subscription.user.email}")