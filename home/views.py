from django.shortcuts import render
from ecommerce.models import Product


def index(request):
    search_term = request.GET.get('search')
    template_data = {}
    if search_term:
        template_data['products'] = Product.objects.filter(name__icontains=search_term)
    else:
        template_data['products'] = Product.objects.all()

    template_data['title'] = 'Project Istmo'
    return render(request, 'home/index.html', {
        'template_data': template_data
    })

def about(request):
    template_data = {}
    template_data['title'] = 'About Istmo'
    return render(request, 'home/about.html', {
        'template_data': template_data
    })