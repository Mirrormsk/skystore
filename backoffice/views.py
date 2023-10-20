from django.shortcuts import render
from django.contrib import messages

from catalog.models import Product, Category


# Create your views here.

def management(request):
    products = Product.objects.all()
    context = {
        'title': 'Управление магазином',
        'object_list': products
    }
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
