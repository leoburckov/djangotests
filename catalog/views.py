from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Контроллер для главной страницы"""
    return render(request, 'home.html')


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