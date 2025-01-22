from django.urls import path
from . import views
from .views import ProductDetailView

urlpatterns = [
    path("", views.home, name="store-home"),
    path("store/", views.store, name="store-list"),
    path('store/<slug:category_slug>/', views.store, name='store-by-category'),  # Filter by category
    path('store/<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product-detail'),
]