# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Skip for these paths
        exempt_paths = [
            '/accounts/',
            '/subscription/',
            '/admin/',
        ]
        
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)
        
        if request.user.is_authenticated:
            # Check if user has an active subscription
            if hasattr(request.user, 'subscription'):
                subscription = request.user.subscription
                
                # Check if subscription has expired
                if subscription.end_date < datetime.now():
                    subscription.is_active = False
                    subscription.save()
                    messages.warning(request, "Tu suscripción ha expirado")
                    return redirect('shop.subscription_plan')
            
            # Redirect to subscription page if no active subscription
            elif not request.path == reverse('shop.subscription_plan'):
                messages.info(request, "Por favor elige un plan para continuar")
                return redirect('shop.subscription_plan')
        
        return self.get_response(request)
