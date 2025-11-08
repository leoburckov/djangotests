from django.urls import path
from .views import (
    IndexView, ProductDetailView, ContactsView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
)

#app_name = 'catalog'  # Это должно быть

urlpatterns = [
    path('', IndexView.as_view(), name='home'),  # Главная страница
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]