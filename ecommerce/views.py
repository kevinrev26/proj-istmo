from django.shortcuts import render
from .models import Product

# Create your views here.
def show_item(request, id):
    product = Product.objects.get(id=id)
    template_data = {}
    template_data['product'] = product
    return render(request, 'ecommerce/show.html', {'template_data' : template_data})