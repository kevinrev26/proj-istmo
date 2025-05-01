from ecommerce.models import Stock
from cart.models import Order
from shop.models import Shop

def dashboard_context(request):
    new_orders_count = 0
    low_stock_count = 0
    if request.user.is_authenticated:
        user_shop = Shop.objects.filter(owner=request.user).first()
        if user_shop:
            new_orders_count = Order.objects.filter(shop=user_shop, status=Order.OrderStatus.PENDING).count()
            low_stock_count = Stock.objects.filter(
                product__shop=user_shop,
                quantity__lt=3
            ).count()


    return {
        'new_orders_count': new_orders_count,
        'low_stock_count': low_stock_count,
        'has_alerts': new_orders_count > 0 or low_stock_count > 0,
    }
