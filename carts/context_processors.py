from .models import Cart, CartItem
from django.db.models import Sum


def cart_counter(request):
    """
    A context processor to provide the cart item count for the navbar.
    """
    cart_count = 0

    try:
        # Check if the user is authenticated
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            # Use session key for anonymous users
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()

        # Calculate the total quantity of items in the cart
        if cart:
            cart_count = (
                CartItem.objects.filter(cart=cart).aggregate(
                    total_items=Sum("quantity")
                )["total_items"]
                or 0
            )
    except Exception as e:
        # Handle exceptions gracefully
        print(f"Error in cart_counter: {e}")

    return {"cart_count": cart_count}
