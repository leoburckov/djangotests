from django.contrib import admin
from django.urls import path, include

from catalog.views import product_detail, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace="catalog")),
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]

