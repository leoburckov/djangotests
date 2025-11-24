# catalog/urls.py
from django.urls import path
from .views import (
    IndexView, ProductDetailView, ContactsView,
    ProductListView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, ProductModerationView,
    CategoryProductsView  # Добавлен импорт
)

app_name = 'catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/moderate/', ProductModerationView.as_view(), name='product_moderation'),
    # Используем ID категории вместо slug
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
]