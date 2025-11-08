from django import forms
from .models import Product
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):
    FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean_name(self):
        name = self.cleaned_data['name']
        return self._check_forbidden_words(name, 'названии')

    def clean_description(self):
        description = self.cleaned_data['description']
        return self._check_forbidden_words(description, 'описании')

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def _check_forbidden_words(self, text, field_name):
        text_lower = text.lower()
        for word in self.FORBIDDEN_WORDS:
            if word in text_lower:
                raise ValidationError(f'Запрещенное слово "{word}" в {field_name}')
        return text