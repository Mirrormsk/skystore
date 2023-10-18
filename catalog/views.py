from django.shortcuts import render
from django.contrib import messages

from .services import messages_saver
from .models import Product, Organization


# Create your views here.


def index(request):
    """Функция отображения главной страницы"""
    context = {
        'nbar': 'home',
        'title': 'Главная',
        'products': Product.objects.all()[:5]
    }

    return render(request, "catalog/index.html", context)


def contacts(request):
    """Функция отображения страницы контактов"""
    if request.method == "POST":
        messages_saver.save_message(request.POST)
        messages.info(request, 'Ваше сообщение принято и будет обработано')

    context = {
        'nbar': 'contacts',
        'title': 'Контакты',
        'organization': Organization.objects.get(pk=1)
    }

    return render(request, "catalog/contacts.html", context)
