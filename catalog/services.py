# catalog/services.py
from django.core.cache import cache
from .models import Product, Category
from django.conf import settings


def get_products_by_category(category_slug):
    """
    Сервисная функция для получения продуктов по категории
    с использованием кеширования
    """
    if settings.CACHE_ENABLED:
        cache_key = f'products_category_{category_slug}'
        products = cache.get(cache_key)
        if products is not None:
            return products

    try:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(
            category=category,
            is_published=True
        ).select_related('category', 'owner')
    except Category.DoesNotExist:
        products = Product.objects.none()

    if settings.CACHE_ENABLED:
        cache_key = f'products_category_{category_slug}'
        cache.set(cache_key, products, 60 * 15)

    return products