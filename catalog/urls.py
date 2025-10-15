from django.urls import path
from .views import home, contacts

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),           # → http://127.0.0.1:8000/
    path('contacts/', contacts, name='contacts'),  # → http://127.0.0.1:8000/contacts/
]