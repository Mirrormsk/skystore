import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone

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


def product(request, pk: int):
    """Функция отображения страницы продукта"""
    # product = Product.objects.get(pk=pk)
    product = get_object_or_404(Product, pk=pk)

    # Info for badge "new"
    is_new = timezone.now() - product.created_at <= datetime.timedelta(days=7)

    context = {
        'title': f'{product.name}',
        'product': product,
        'is_new': is_new
    }

    return render(request, "catalog/product.html", context)
