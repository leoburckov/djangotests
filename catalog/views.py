from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm, ProductModerationForm


class ProductOwnerMixin(UserPassesTestMixin):
    """Миксин для проверки владельца продукта"""

    def test_func(self):
        product = self.get_object()
        return product.can_edit(self.request.user)


class ProductDeleteMixin(UserPassesTestMixin):
    """Миксин для проверки прав на удаление"""

    def test_func(self):
        product = self.get_object()
        return product.can_delete(self.request.user)


class IndexView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # ВРЕМЕННОЕ РЕШЕНИЕ: используем только существующие поля
        # Пока не применены миграции для owner_id
        try:
            # Пытаемся получить продукты без обращения к owner
            return Product.objects.all()[:6]
        except Exception as e:
            # Если ошибка, возвращаем пустой queryset
            print(f"Error in IndexView: {e}")
            return Product.objects.none()


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # ВРЕМЕННОЕ РЕШЕНИЕ: убираем фильтр по is_published
        try:
            return Product.objects.all()
        except Exception as e:
            print(f"Error in ProductListView: {e}")
            return Product.objects.none()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Безопасное получение объекта
        try:
            return super().get_object(queryset)
        except Exception as e:
            print(f"Error in ProductDetailView: {e}")
            return None


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
        try:
            # ВРЕМЕННО: проверяем есть ли поле owner перед установкой
            if hasattr(form.instance, 'owner'):
                form.instance.owner = self.request.user
            if hasattr(form.instance, 'status'):
                form.instance.status = 'moderation'
            if hasattr(form.instance, 'is_published'):
                form.instance.is_published = False
            messages.success(self.request, 'Продукт успешно создан!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Ошибка при создании продукта: {e}')
            return self.form_invalid(form)


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
        try:
            # ВРЕМЕННО: проверяем наличие полей
            if (hasattr(form.instance, 'status') and
                    hasattr(form.instance, 'is_published') and
                    form.instance.status == 'published'):
                form.instance.status = 'moderation'
                form.instance.is_published = False
            messages.success(self.request, 'Продукт успешно обновлен!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Ошибка при обновлении продукта: {e}')
            return self.form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, ProductDeleteMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно удален!')
        return super().form_valid(form)


class ProductModerationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Представление для модерации продуктов"""
    model = Product
    form_class = ProductModerationForm
    template_name = 'catalog/product_moderation.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        return self.request.user.has_perm('catalog.can_change_status')

    def form_valid(self, form):
        try:
            product = form.save(commit=False)
            # ВРЕМЕННО: проверяем наличие полей
            if (hasattr(product, 'status') and
                    hasattr(product, 'is_published')):
                if product.status == 'published':
                    product.is_published = True
                else:
                    product.is_published = False
            product.save()
            messages.success(self.request, f'Статус продукта изменен на "{product.get_status_display()}"')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Ошибка при модерации продукта: {e}')
            return self.form_invalid(form)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class SafeIndexView(TemplateView):
    """Безопасная версия главной страницы без запросов к БД"""
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Временно передаем пустой список продуктов
        context['products'] = []
        return context