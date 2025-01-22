from .models import Category
from django.db.models import Count
from django.core.cache import cache


def store_categories_processor(request):
    """
    Context processor to include all categories for the store in the template context.
    """
    categories = Category.objects.all()
    return {"store_categories": categories}  # Use a more descriptive name


def top_categories_processor(request):
    top_categories = cache.get("top_categories")
    if not top_categories:
        top_categories = (
            Category.objects.annotate(product_count=Count("product"))
            .filter(product_count__gt=0)
            .order_by("-product_count")[:6]
        )
        cache.set("top_categories", top_categories, 300)  # Cache for 5 minutes
    return {"top_categories": top_categories}
