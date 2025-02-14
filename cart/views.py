from django.shortcuts import render, get_object_or_404, redirect
from ecommerce.models import Product
from .utils import calculate_cart_total

def add(request, id):
    get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def index(request):
    cart_total = 0
    products_in_cart = []
    cart = request.session.get('cart', {})
    product_ids = list(cart.keys())
    if (product_ids != []):
        products_in_cart = Product.objects.filter(id__in=product_ids)
        cart_total = calculate_cart_total(cart, products_in_cart)
    
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['products_in_cart'] = products_in_cart
    template_data['cart_total'] = cart_total

    return render(request, 'cart/index.html', {'template_data': template_data})

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')