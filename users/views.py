from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.views import View
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

        # Отправка приветственного письма
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


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.get_user().email}!')
        return super().form_valid(form)


class UserLogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, 'Вы успешно вышли из системы.')
        return redirect('catalog:home')

    def get(self, request):
        logout(request)
        messages.info(request, 'Вы успешно вышли из системы.')
        return redirect('catalog:home')