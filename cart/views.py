from django.shortcuts import render, get_object_or_404, redirect
from ecommerce.models import Product
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

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

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    product_ids = list(cart.keys())

    if (product_ids == []):
        return redirect('cart.index')
    
    products_in_cart = Product.objects.filter(id__in=product_ids)
    cart_total = calculate_cart_total(cart, products_in_cart)

    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()

    for product in products_in_cart:
        item = Item()
        item.product = product
        item.price = product.price
        item.order = order
        item.quantity = cart[str(product.id)]
        item.save()
    
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html', {'template_data': template_data})