from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from blog.models import Article
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
    product_item.is_active = not product_item.is_active

    product_item.save()

    return redirect(reverse_lazy('backoffice:backoffice'))


def toggle_article_activity(request, pk):
    article_item = get_object_or_404(Article, pk=pk)
    article_item.is_published = not article_item.is_published
    article_item.save()

    return redirect(reverse_lazy('backoffice:blog_list'))


class BackofficeProductListView(ListView):
    model = Product
    template_name = 'backoffice/backoffice_products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['categories'] = Category.objects.all()
        context_data['title'] = 'Товары'
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


class BackofficeArticleListView(ListView):
    model = Article

    template_name = 'backoffice/backoffice_articles.html'
    extra_context = {
        'title': 'Статьи',
        'nbar': 'backoffice'
    }


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('backoffice:blog_list')

    extra_context = {
        'title': 'Удаление статьи'
    }
