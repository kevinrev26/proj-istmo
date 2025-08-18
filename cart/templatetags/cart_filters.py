from django import template

register = template.Library()

@register.filter(name='get_quantity')
def get_cart_quantity(cart, product_id):
    print("What is this fucking cart:")
    print(cart)
    return cart.get(str(product_id), 0)

@register.filter(name='multiply')
def multiply(price, quantity):
    try:
        return price * quantity
    except (TypeError, ValueError):
        return 0