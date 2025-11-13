from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'avatar':
                field.widget.attrs.update({'class': 'form-control'})
            elif field_name == 'email':
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Введите ваш email',
                    'autofocus': True
                })
            elif 'password' in field_name:
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Введите пароль'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg',
                    'placeholder': f'Введите {field.label.lower()}'
                })

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'phone', 'country', 'avatar')
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}),
            'country': forms.TextInput(attrs={'placeholder': 'Ваша страна'}),
        }

