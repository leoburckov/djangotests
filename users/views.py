from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserRegisterForm
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        # Отправка приветственного письма (в консоль для тестов)
        try:
            send_mail(
                subject='Добро пожаловать в наш магазин!',
                message=f'Уважаемый(ая) {user.email}, спасибо за регистрацию в нашем магазине!',
                from_email='noreply@myshop.com',
                recipient_list=[user.email],
                fail_silently=True,
            )
            messages.success(self.request, 'Регистрация успешна! На ваш email отправлено приветственное письмо.')
        except Exception as e:
            messages.success(self.request, f'Регистрация успешна! (Ошибка отправки email: {e})')

        # Автоматический вход после регистрации
        login(self.request, user)
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('catalog:home')

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.get_user().email}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный email или пароль.')
        return super().form_invalid(form)


from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)