from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),  # Подключаем URLs каталога
    path('blog/', include('blog.urls')),  # Подключаем URLs блога
    path('users/', include('users.urls')),
]