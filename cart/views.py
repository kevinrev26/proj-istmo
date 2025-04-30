from django.shortcuts import render, get_object_or_404, redirect
from ecommerce.models import Product
from ecommerce.models import Shop
from collections import defaultdict
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
    products = Product.objects.filter(id__in=product_ids)

    if (product_ids == []):
        return redirect('cart.index')
    
    # Group products by shop
    shop_products = defaultdict(list)
    for product in products:
        shop_products[product.shop.id].append(product)

    created_orders = []

    for shop_id, products_in_shop in shop_products.items():
        
        shop = Shop.objects.get(id=shop_id)
        
        order_total = calculate_cart_total(cart, products_in_shop)

        order = Order.objects.create(
            user=request.user,
            total=order_total,
            shop=shop,
        )
        created_orders.append(order)

        for product in products_in_shop:
            #TODO Decrease Stock quantity
            Item.objects.create(
                product=product,
                quantity=cart[str(product.id)],
                price=product.price,
                order=order
            )

    # Clear the cart
    request.session['cart'] = {}

    return render(request, 'cart/purchase.html', {
        'title': 'Purchase Confirmation',
        # Leave the orders here to make use in the future.
        'orders': created_orders,
    })
