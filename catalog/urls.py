from django.urls import path
from .views import (
    IndexView, ProductDetailView, ContactsView,
    ProductListView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, ProductModerationView,
    SafeIndexView  # Добавьте эту строку для временного использования
)

app_name = 'catalog'

urlpatterns = [
    # ВРЕМЕННО: используем безопасную версию главной страницы
    # чтобы избежать ошибок с owner_id до применения миграций
    path('', SafeIndexView.as_view(), name='home'),

    # ОРИГИНАЛЬНАЯ версия (закомментирована до решения проблемы с миграциями)
    # path('', IndexView.as_view(), name='home'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/moderate/', ProductModerationView.as_view(), name='product_moderation'),
]