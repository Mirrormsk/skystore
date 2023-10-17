from django.shortcuts import render
from django.contrib import messages

from .services import messages_saver
from .models import Product, Organization


# Create your views here.


def index(request):
    """Функция отображения главной страницы"""
    return render(request, "catalog/index.html", {'nbar': 'home', 'products': Product.objects.all()[:5]})


def contacts(request):
    """Функция отображения страницы контактов"""
    if request.method == "POST":
        messages_saver.save_message(request.POST)
        messages.info(request, 'Ваше сообщение принято и будет обработано')

    return render(request, "catalog/contacts.html", {'nbar': 'contacts', 'organization': Organization.objects.get(pk=1)})
