# utils.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_activation_email(user, activation_url):
    subject = "Activa tu cuenta en IstmoPay"
    
    # Render HTML template
    html_content = render_to_string('emails/account_activation.html', {
        'user': user,
        'activation_url': activation_url,
    })
    
    # Create text version
    text_content = strip_tags(html_content)
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
