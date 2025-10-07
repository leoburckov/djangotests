from django.urls import path
from . import views
from .views import contacts, home

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
]
