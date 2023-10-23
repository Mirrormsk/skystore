from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from catalog.models import Product, Category


class ProductCreateView(CreateView):
    model = Product

    fields = ('name', 'description', 'preview', 'category', 'price')

    success_url = reverse_lazy('backoffice:backoffice')

    extra_context = {
        'title': 'Создать новый продукт',
        'categories': Category.objects.all()
    }


class ProductUpdateView(UpdateView):
    model = Product

    fields = ('name', 'description', 'preview', 'category', 'price')

    success_url = reverse_lazy('backoffice:backoffice')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        categories = Category.objects.all()

        context_data['categories'] = categories
        context_data['title'] = f'Редактирование товара {product.name}'

        return context_data


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('backoffice:backoffice')
    extra_context = {
        'title': 'Удаление товара'
    }


def toggle_product_activity(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.is_active:
        product_item.is_active = False
    else:
        product_item.is_active = True
    product_item.save()

    return redirect(reverse_lazy('backoffice:backoffice'))


class BackofficeListView(ListView):
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        categories = Category.objects.all()


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
