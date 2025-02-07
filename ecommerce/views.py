from django.shortcuts import render
from ecommerce.common import get_product_by_id

# Create your views here.
def show_item(request, id):
    product = get_product_by_id(id)
    template_data = {}
    template_data['product'] = product
    return render(request, 'ecommerce/show.html', {'template_data' : template_data})