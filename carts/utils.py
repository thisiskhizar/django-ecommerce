# carts/utils.py
from .models import Cart, CartItem


def get_or_create_cart(user=None, session_key=None):
    if user and user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
    else:
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def add_to_cart(cart, product, quantity=1):
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    cart_item.save()
    return cart_item


def remove_from_cart(cart, product):
    CartItem.objects.filter(cart=cart, product=product).delete()


def get_cart_total(cart):
    return sum(item.total_price for item in cart.items.all())
