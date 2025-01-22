from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
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