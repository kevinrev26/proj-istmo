def calculate_cart_total(cart, products_in_cart):
    total = 0
    for product in products_in_cart:
        quantity = cart[str(product.id)]
        total += product.price * int(quantity)

    return total