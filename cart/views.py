from django.shortcuts import render, get_object_or_404, redirect
from ecommerce.models import Product, StockMovement, Shop
from collections import defaultdict
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

def add(request, id):
    get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})
    # Standardize to string keys
    cart[str(id)] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def index(request):
    cart_total = 0
    products_in_cart = []
    cart = request.session.get('cart', {})
    
    # Convert all keys to strings for consistency
    str_cart = {str(k): v for k, v in cart.items()}
    request.session['cart'] = str_cart  # Update session with string keys
    
    product_ids = list(str_cart.keys())
    if product_ids:
        products_in_cart = Product.objects.filter(id__in=product_ids)
        cart_total = calculate_cart_total(str_cart, products_in_cart)
    
    template_data = {
        'title': 'Cart',
        'products_in_cart': products_in_cart,
        'cart_total': cart_total,
        'cart': str_cart  # Pass the standardized cart to the template
    }

    return render(request, 'cart/index.html', {'template_data': template_data})

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    str_cart = {str(k): v for k, v in cart.items()}
    product_ids = list(str_cart.keys())
    
    if not product_ids:
        return redirect('cart.index')
    
    products = Product.objects.filter(id__in=product_ids)
    
    # Group products by shop
    shop_products = defaultdict(list)
    for product in products:
        shop_products[product.shop.id].append(product)

    created_orders = []

    for shop_id, products_in_shop in shop_products.items():
        shop = Shop.objects.get(id=shop_id)
        order_total = calculate_cart_total(str_cart, products_in_shop)  # Use str_cart here

        order = Order.objects.create(
            user=request.user,
            total=order_total,
            shop=shop,
        )
        created_orders.append(order)

        for product in products_in_shop:
            qty = str_cart[str(product.id)]  # Use str_cart here
            stock = product.stock
            stock.quantity = stock.quantity - int(qty)
            stock.save()

            stock_movement = StockMovement(
                product=product,
                movement_type='outgoing',
                quantity=qty
            )
            stock_movement.save()
            
            Item.objects.create(
                product=product,
                quantity=qty,
                price=product.price,
                order=order
            )

    request.session['cart'] = {}
    return render(request, 'cart/purchase.html', {
        'title': 'Purchase Confirmation',
        'orders': created_orders,
    })
