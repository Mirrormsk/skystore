import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .services import messages_saver
from .models import Product, Organization, Category


# Create your views here.


def index(request):
    """Функция отображения главной страницы"""
    context = {
        'nbar': 'home',
        'title': 'Главная',
        'products': Product.objects.all()
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


def management(request):
    products = Product.objects.all()
    context = {
        'title': 'Управление магазином',
        'object_list': products
    }
    return render(request, 'catalog/management_products.html', context)


def add_product(request):
    if request.method == 'POST':

        print(request.POST)
        new_product = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'price': request.POST.get('price'),
            'category': Category.objects.get(pk=request.POST.get('category'))
        }
        if request.FILES:
            print(request.FILES)
            new_product.update({
                'preview': request.FILES.get('preview')
            })
        try:
            Product.objects.create(**new_product)
            messages.info(request, 'Товар успешно создан!')
        except:
            messages.info(request, 'Ошибка создания товара')

    context = {
        'title': 'Добавить товар',
        'categories': Category.objects.all()
    }
    return render(request, 'catalog/add_product.html', context)
