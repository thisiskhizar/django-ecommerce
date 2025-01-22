# carts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart, CartItem
from store.models import Product
from .utils import get_or_create_cart, add_to_cart, remove_from_cart


def cart_detail_view(request):
    session_key = request.session.session_key or request.session.create()
    cart = get_or_create_cart(user=request.user, session_key=session_key)
    context = {
        "cart": cart,
        "total": sum(item.total_price for item in cart.items.all()),
    }
    return render(request, "store/cart-detail.html", context)


def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart = get_or_create_cart(user=request.user, session_key=session_key)
    add_to_cart(cart, product)
    return redirect("cart-detail")


def remove_from_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key or request.session.create()
    cart = get_or_create_cart(user=request.user, session_key=session_key)
    remove_from_cart(cart, product)
    return redirect("cart-detail")


def decrement_cart_item(request, product_id):
    """Decrement the quantity of a cart item."""
    # Ensure the session key is set
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    product = get_object_or_404(Product, id=product_id)

    # Retrieve the correct cart for the user or session
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=session_key).first()

    if not cart:
        # No cart exists; redirect back to cart page
        return redirect('cart-detail')

    # Find the cart item
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # If quantity is 1, remove the item
            cart_item.delete()

    return redirect('cart-detail')
