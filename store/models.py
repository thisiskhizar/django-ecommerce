from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Custom Validator for Image Size
def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5 MB limit
    if image.size > max_size:
        raise ValidationError(_("Image file size should be under 5MB"))


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Category Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Category Description")
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        validators=[validate_image_size],
        verbose_name="Category Image",
    )

    # Automatically generate slug from name field before saving
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_url(self):
        return reverse("store-by-category", args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]  # Sort categories by name in queries
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={
            'category_slug': self.category.slug,
            'product_slug': self.slug
        })