from django.shortcuts import render
from ecommerce.models import Product
from django.utils import timezone
from datetime import timedelta
from shop.models import Shop


def index(request):
    search_term = request.GET.get('search')
    template_data = {}
    if search_term:
        template_data['products'] = Product.objects.filter(name__icontains=search_term)
    else:
        template_data['products'] = Product.objects.all()

    fifteen_days_ago = timezone.now() - timedelta(days=15)
    latest_shops = Shop.objects.filter(
        created_at__gte=fifteen_days_ago
    ).order_by('-created_at')[:5]

    template_data['title'] = 'Project Istmo'
    return render(request, 'home/index.html', {
        'template_data': template_data,
        'latest_shops' : latest_shops
    })

def about(request):
    template_data = {}
    template_data['title'] = 'About Istmo'
    return render(request, 'home/about.html', {
        'template_data': template_data
    })