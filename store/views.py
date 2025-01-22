from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView

from carts.models import Cart, CartItem
from .models import Category, Product


def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        "products": products,
    }
    return render(request, "store/index.html", context)


def store(request, category_slug=None):
    category = None
    products = Product.objects.filter(is_available=True).order_by("-created_at")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_count = products.count()
    context = {
        "products": products,
        "product_count": product_count,
        "category": category,  # To show active category if applicable
        "categories": Category.objects.all(),  # To list all categories in the template
    }
    return render(request, "store/store-list.html", context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product-detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Get the category by slug
        category_slug = self.kwargs.get('category_slug')
        product_slug = self.kwargs.get('product_slug')

        # Get the category object
        category = get_object_or_404(Category, slug=category_slug)

        # Get the product object by its slug and ensure it belongs to the correct category
        product = get_object_or_404(Product, slug=product_slug, category=category)

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the product from the context
        product = self.get_object()

        # Determine the cart based on the user or session
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            session_key = self.request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()

        # Check if the product is in the cart
        in_cart = False
        if cart:
            in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

        # Add `in_cart` to the context
        context['in_cart'] = in_cart

        return context