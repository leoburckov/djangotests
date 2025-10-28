from django.shortcuts import render
from django.http import HttpResponse

from catalog.models import Product


def home(request):
    """Контроллер для главной страницы"""
    products = Product.objects.all()[:6]  # Получаем первые 6 товаров
    context = {
        'products': products,
        'title': 'Главная страница'
    }
    return render(request, 'home.html', context)


def contacts(request):
    """Контроллер для страницы контактов"""
    if request.method == 'POST':
        # Обработка данных формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Здесь можно добавить логику сохранения или отправки email
        print(f"Получено сообщение от {name}, телефон: {phone}")
        print(f"Сообщение: {message}")

        # Можно добавить редирект после успешной отправки
        # return HttpResponseRedirect('/contacts/')

    return render(request, 'contacts.html')

def product_detail(request, pk):
    """Контроллер для страницы одного товара"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'title': f'Товар - {product.name}'
    }
    return render(request, 'catalog/product_detail.html', context)