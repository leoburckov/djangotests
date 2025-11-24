# catalog/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.conf import settings

from .models import Product, Category
from .forms import ProductForm, ProductModerationForm
from .services import get_products_by_category  # Импорт сервисной функции


class ProductOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        product = self.get_object()
        return product.can_edit(self.request.user)


class ProductDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        product = self.get_object()
        return product.can_delete(self.request.user)


# КЕШИРОВАНИЕ ГЛАВНОЙ СТРАНИЦЫ
class IndexView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        if settings.CACHE_ENABLED:
            cache_key = 'home_products'
            products = cache.get(cache_key)
            if products is not None:
                return products

        products = Product.objects.all().select_related('category')[:6]

        if settings.CACHE_ENABLED:
            cache_key = 'home_products'
            cache.set(cache_key, products, 60 * 10)  # 10 минут

        return products


# КЕШИРОВАНИЕ СПИСКА ПРОДУКТОВ
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        if settings.CACHE_ENABLED:
            cache_key = 'all_products'
            products = cache.get(cache_key)
            if products is not None:
                return products

        products = Product.objects.all().select_related('category')

        if settings.CACHE_ENABLED:
            cache_key = 'all_products'
            cache.set(cache_key, products, 60 * 10)  # 10 минут

        return products


# КЕШИРОВАНИЕ СТРАНИЦЫ ПРОДУКТА
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# КЕШИРОВАНИЕ ПРОДУКТОВ ПО КАТЕГОРИИ
class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)  # Используем сервисную функцию

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['category'] = get_object_or_404(Category, id=category_id)
        return context


# ОСТАЛЬНЫЕ КЛАССЫ БЕЗ ИЗМЕНЕНИЙ
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, ProductOwnerMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = '/users/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно обновлен!')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, ProductDeleteMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно удален!')
        return super().form_valid(form)


class ProductModerationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductModerationForm
    template_name = 'catalog/product_moderation.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Продукт обновлен!')
        return super().form_valid(form)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'