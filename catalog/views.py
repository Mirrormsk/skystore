import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Product, Organization
from .services import messages_saver


def index(request):
    """Функция отображения главной страницы"""
    objects = Product.objects.all()
    pagen = Paginator(objects, 5)
    page = request.GET.get('page')

    if not page:
        page = 1

    context = {
        'nbar': 'home',
        'title': 'Главная',
        'products': pagen.page(page).object_list,
        'page': pagen.page(page),
        'paginator': pagen
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

    # Recommended
    recommended = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]

    context = {
        'title': f'{product.name}',
        'product': product,
        'is_new': is_new,
        'recommended': recommended
    }

    return render(request, "catalog/product.html", context)
