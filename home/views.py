from django.shortcuts import render
from ecommerce.common import get_products


def index(request):
    template_data = {}
    template_data['title'] = 'Project Istmo'
    template_data['products'] = get_products()
    return render(request, 'home/index.html', {
        'template_data': template_data
    })

def about(request):
    template_data = {}
    template_data['title'] = 'About Istmo'
    return render(request, 'home/about.html', {
        'template_data': template_data
    })