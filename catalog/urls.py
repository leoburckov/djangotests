from django.urls import path
from .views import IndexView, ProductDetailView, ContactsView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]