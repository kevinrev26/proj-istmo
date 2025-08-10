from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def user_has_active_subscription(user):
    return hasattr(user, 'subscription') and user.subscription.is_active

@register.simple_tag
def user_has_active_trial(user):
    return hasattr(user, 'subscription') and user.subscription.is_trial and user.subscription.is_active

@register.simple_tag
def user_subscription_plan(user):
    if hasattr(user, 'subscription'):
        return user.subscription.plan.name
    return None

@register.simple_tag
def days_remaining(user):
    if hasattr(user, 'subscription'):
        return (user.subscription.end_date - datetime.now()).days
    return 0