from django.shortcuts import render, redirect
from django.contrib import messages

from catalog.models import Product, Category


# Create your views here.

def backoffice(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_pk = 0

    if request.method == 'POST':
        category_pk = request.POST.get('category')

        if category_pk != '0':
            products = Product.objects.filter(category=Category.objects.get(pk=category_pk))

    context = {
        'title': 'Управление магазином',
        'object_list': products,
        'categories': categories,
        'selected_category_pk': int(category_pk)
    }
    print(context)
    return render(request, 'backoffice/management_products.html', context)


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
    return render(request, 'backoffice/add_product.html', context)


def edit_product(request, product_pk):
    # todo: доделать изменение фото
    product = Product.objects.get(pk=product_pk)
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
