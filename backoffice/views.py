from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from catalog.models import Product, Category
from .forms.product_form import ProductForm


def backoffice(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_pk = 0

    if request.method == 'POST':
        category_pk = request.POST.get('category')

        categories_pk_list = list(Category.objects.values_list('pk', flat=True))

        if int(category_pk) in categories_pk_list:
            products = Product.objects.filter(category=Category.objects.get(pk=category_pk))

    context = {
        'nbar': 'backoffice',
        'title': 'Управление магазином',
        'object_list': products,
        'categories': categories,
        'selected_category_pk': int(category_pk)
    }
    return render(request, 'backoffice/management_products.html', context)


def add_product(request):
    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            messages.info(request, 'Товар успешно создан!')
        else:
            messages.info(request, f'Ошибка создания товара')

    else:
        form = ProductForm()

    context = {
        'title': 'Добавить товар',
        'categories': Category.objects.all(),
        'form': form,
    }
    return render(request, 'backoffice/add_product.html', context)


def edit_product(request, product_pk):
    # todo: доделать изменение фото
    product = get_object_or_404(Product, pk=product_pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category = Category.objects.get(pk=request.POST.get('category'))
        product.save()
        return redirect('backoffice:backoffice')

    context = {
        'title': f'Редактировать товар - {product.name}',
        'product': product,
        'categories': Category.objects.all(),
        'selected_category_pk': product.category.pk
    }
    return render(request, 'backoffice/edit.html', context)
