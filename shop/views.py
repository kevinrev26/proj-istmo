from django.shortcuts import render, redirect, get_object_or_404
from .models import Shop
from ecommerce.models import Product, Stock, StockMovement
from cart.models import Order, Item
from django.contrib.auth.decorators import login_required
from .forms import ShopForm, ProductForm
from django.utils.timezone import now
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def show(request):
    user_shop = Shop.objects.filter(owner=request.user).first()
    print(user_shop)
    if not user_shop:
        if request.method == "POST":
            form = ShopForm(request.POST, request.FILES)
            if form.is_valid():
                # So if you commit=False, the form is save in "memory" onlt
                shop = form.save(commit=False)
                shop.owner = request.user
                shop.save()
                return redirect('shop.show')
            else:
                template_data = {}
                template_data['form'] = form
                return render(request, 'shop/shop_creation.html', {'template_data': template_data})
        else:
            form = ShopForm()
            template_data = {}
            template_data['form'] = form
            return render(request, 'shop/shop_creation.html', {'template_data': template_data})
    else:
        return render(request, 'shop/show.html', {'shop': user_shop})


@login_required
def show_orders(request):
    user_shop = Shop.objects.filter(owner=request.user).first()
    #TODO Validate when there is no user shop.
    orders = Order.objects.filter(shop=user_shop)
    return render(request, 'shop/orders.html', {'orders': orders})

@login_required
def show_order_details(request, order_id):
    #TODO: Validate if order exists
    order = Order.objects.get(id=order_id)
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            new_status = int(request.POST.get('status'))
            #TODO Check for Delivred or Done status, to send electronic biling
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
        except Exception as e:
            messages.error(request, 'Error updating order: ' + str(e))
    return redirect('shop.order_detail', order_id=order_id)

@login_required
def show_inventory(request):
    user_shop = Shop.objects.filter(owner=request.user).first()
    products = user_shop.products.all()
    data = []
    for product in products:
        # This is returning a tuple, (obj, created), so unpack is needed
        stock, _ = Stock.objects.get_or_create(product=product)
        data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': stock.quantity,
            'last_updated': stock.last_updated,
        })
    return render(request, 'shop/inventory.html', {'shop': user_shop, 'products' : data})

@login_required
def show_chat(request):
    user_shop = Shop.objects.filter(owner=request.user).first()
    return render(request, 'shop/chat.html', {'shop': user_shop})

@login_required
def add_product(request):
    template_data = {}
    template_data['title'] = 'Add Product'
    
    if request.method == 'GET':
        form = ProductForm()
        template_data['form'] = form
        return render(request, 'shop/add_product.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            user_shop = Shop.objects.filter(owner=request.user).first()
            product.shop = user_shop
            product.save()
            return redirect('shop.inventory')
        else:
            template_data = {}
            template_data['form'] = form
            return render(request, 'shop/add_product.html', {'template_data': template_data})

@login_required
def add_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 0))
        if qty > 0:
            stock, _ = Stock.objects.get_or_create(product=product)
            stock.quantity += qty
            stock.last_updated = now()
            stock.save()
            stock_movement = StockMovement(
                product=product,
                movement_type='incoming',
                quantity=qty
            )
            stock_movement.save()
            return redirect('shop.inventory')
