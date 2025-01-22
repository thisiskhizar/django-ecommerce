from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail_view, name="cart-detail"),
    path("add/<int:product_id>/", views.add_to_cart_view, name="add-to-cart"),
    path(
        "remove/<int:product_id>/", views.remove_from_cart_view, name="remove-from-cart"
    ),
    path('decrement/<int:product_id>/', views.decrement_cart_item, name='decrement-cart-item'),  # New
]
