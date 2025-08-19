from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Shop, Subscription, SubscriptionPlan
from ecommerce.models import Product, Stock, StockMovement, Category
from cart.models import Order, Item
from django.contrib.auth.decorators import login_required
from .forms import ShopForm, ProductForm
from django.utils.timezone import now
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum, Avg
from django.core.paginator import Paginator
from .helpers import get_current_and_previous_days, get_sales_rate

@login_required
def show(request):
    user_shop = Shop.objects.filter(owner=request.user).first()
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
            template_data['categories'] = Category.objects.filter(parent__isnull=True)
            return render(request, 'shop/shop_creation.html', {'template_data': template_data})
    else:
        # Get orders and other stuff for the dashboard.
        template_data = {}
        template_data['shop'] = user_shop

        #TODO Refactor into a helper function
        new_orders_count = Order.objects.filter(shop=user_shop, status=Order.OrderStatus.IN_PROCESS).count()
        orders_processed = Order.objects.filter(shop=user_shop).exclude(
                status__in = [
                    Order.OrderStatus.PENDING,
                    Order.OrderStatus.IN_PROCESS
                ]
        ).count()
        total_dispatched = Order.objects.filter(shop=user_shop, status=Order.OrderStatus.DISPATCHED).count()
        orders_canceled = Order.objects.filter(shop=user_shop, status=Order.OrderStatus.CANCELED).count()
        total_sales = Order.objects.filter(shop=user_shop, status=Order.OrderStatus.DONE).aggregate(
            total=Sum('total'))['total'] or 0

        str_prv_month, end_prv_month, str_curr_month = get_current_and_previous_days()

        current_month_sales = Order.objects.filter(
            shop=user_shop,
            status=Order.OrderStatus.DONE,
            date__gte=str_curr_month
        ).aggregate(total=Sum('total'))['total'] or 0

        previous_month_sales = Order.objects.filter(
            shop=user_shop,
            status=Order.OrderStatus.DONE,
            date__gte=str_prv_month,
            date__lte=end_prv_month
        ).aggregate(total=Sum('total'))['total'] or 0
        
        rate, rate_class = get_sales_rate(previous_month_sales, current_month_sales)

        avg_month_orders = Order.objects.filter(
            shop=user_shop,
            status=Order.OrderStatus.DONE,
            date__gte=str_curr_month
        ).aggregate(total=Avg('total'))['total'] or 0

        avg_previous_month_orders = Order.objects.filter(
            shop=user_shop,
            status=Order.OrderStatus.DONE,
            date__gte=str_prv_month,
            date__lte=end_prv_month
        ).aggregate(total=Avg('total'))['total'] or 0
        
        avg_rate, avg_rate_class = get_sales_rate(avg_previous_month_orders, avg_month_orders)

        template_data['new_orders_count'] = new_orders_count
        template_data['orders_processed'] = orders_processed
        template_data['total_dispatched'] = total_dispatched
        template_data['orders_canceled'] = orders_canceled
        template_data['total_sales'] = total_sales
        template_data['rate'] = rate
        template_data['rate_class'] = rate_class
        template_data['avg_month_orders'] = avg_month_orders
        template_data['avg_rate'] = avg_rate
        template_data['avg_rate_class'] = avg_rate_class
        template_data['shop'] = user_shop 
        return render(request, 'shop/show.html', {'template_data': template_data})

@login_required
def show_orders(request):
    user_shop = Shop.objects.filter(owner=request.user).first()
    if not user_shop:
        return redirect('shop.show')
    
    orders = Order.objects.filter(shop=user_shop).order_by('-date')
    
    # Get filter parameters
    customer = request.GET.get('customer', '')
    status = request.GET.get('status', '')
    date_range = request.GET.get('date_range', '')
    
    # Apply filters
    if customer:
        orders = orders.filter(
            Q(user__username__icontains=customer) |
            Q(user__email__icontains=customer)
        )
    
    if status:
        orders = orders.filter(status=status)
    
    if date_range:
        today = timezone.now().date()
        if date_range == 'today':
            orders = orders.filter(date__date=today)
        elif date_range == 'week':
            orders = orders.filter(date__date__gte=today - timedelta(days=7))
        elif date_range == 'month':
            orders = orders.filter(date__date__gte=today - timedelta(days=30))
        elif date_range == 'year':
            orders = orders.filter(date__date__gte=today - timedelta(days=365))
    
    # Pagination
    paginator = Paginator(orders, 25)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    # Get status choices from model
    status_choices = Order.OrderStatus.choices
    
    context = {
        'orders': orders,
        'status_choices': status_choices,
    }
    return render(request, 'shop/orders.html', context)

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
            'image' : product.image,
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
        template_data['subcategories'] = Category.objects.filter(parent__isnull=False)
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

@login_required
def show_subcription_plan(request):
    user = request.user
    template_data = {
        'user' : user,
    }
    return render(request, 'shop/subscription_plan.html', {'template_data': template_data})

@login_required
def start_trial(request, plan):
    # Get the requested plan
    plan_obj = get_object_or_404(SubscriptionPlan, slug=plan)
    
    # Check if user already has an active subscription
    if hasattr(request.user, 'subscription'):
        messages.warning(request, "Ya tienes una suscripción activa")
        return redirect('shop.dashboard')
    
    # Create trial subscription
    trial_end_date = datetime.now() + timedelta(days=30)
    
    Subscription.objects.create(
        user=request.user,
        plan=plan_obj,
        is_trial=True,
        is_active=True,
        start_date=datetime.now(),
        end_date=trial_end_date,
        next_billing_date=trial_end_date
    )
    
    messages.success(request, f"¡Prueba gratuita de {plan_obj.name} activada por 30 días!")
    return redirect('shop.show')

def store_front(request, store_slug):
    shop = get_object_or_404(Shop, slug=store_slug)
    products = Product.objects.filter(shop=shop)
    
    return render(request, 'store/front.html', {
        'shop': shop,
        'products': products,
        'template_data': {
            'title': shop.name,
            'description': shop.description,
        }
    })

@login_required
def stock_movements(request):
    # Default filter - last 30 days
    date_filter = request.GET.get('date_filter', '30days')
    product_name = request.GET.get('product_name', '')
    user_shop = Shop.objects.filter(owner=request.user).first()
    # Base queryset
    movements = StockMovement.objects.filter(product__shop=user_shop)
    
    # Apply date filters
    today = timezone.now().date()
    if date_filter == 'today':
        movements = movements.filter(date__date=today)
    elif date_filter == '7days':
        movements = movements.filter(date__date__gte=today - timedelta(days=7))
    elif date_filter == '30days':
        movements = movements.filter(date__date__gte=today - timedelta(days=30))
    elif date_filter == 'all':
        pass  # No date filter
    
    # Apply product name filter
    if product_name:
        movements = movements.filter(
            Q(product__name__icontains=product_name) |
            Q(product__id__icontains=product_name)
        )
    
    # Group by date for display
    grouped_movements = {}
    for movement in movements.order_by('-date'):
        date_str = movement.date.strftime('%Y-%m-%d')
        if date_str not in grouped_movements:
            grouped_movements[date_str] = []
        grouped_movements[date_str].append(movement)
    
    context = {
        'grouped_movements': grouped_movements,
        'date_filter': date_filter,
        'product_name': product_name,
        'date_options': [
            ('today', 'Today'),
            ('7days', 'Last 7 Days'),
            ('30days', 'Last 30 Days'),
            ('all', 'All Time'),
        ]
    }
    return render(request, 'shop/stock_movements.html', context)
 