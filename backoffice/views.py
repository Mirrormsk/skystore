from django.shortcuts import redirect, get_object_or_404
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
    template_name = 'backoffice/management_products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['categories'] = Category.objects.all()
        context_data['title'] = 'Управление магазином'
        context_data['nbar'] = 'backoffice'
        context_data['selected_category_pk'] = int(self.request.POST.get('category', 0))

        return context_data

    def get_queryset(self):
        category_pk = self.request.POST.get('category', 0)

        categories_pk_list = list(Category.objects.values_list('pk', flat=True))

        if int(category_pk) in categories_pk_list:
            return self.model.objects.filter(category_id=category_pk)
        return self.model.objects.all()

    def post(self, request):
        return self.get(request)
