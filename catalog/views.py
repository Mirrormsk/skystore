import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .models import Product, Organization
from .services import messages_saver


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    paginate_by = 5


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        product = Product.objects.get(pk=self.kwargs.get('pk'))
        is_new = timezone.now() - product.created_at <= datetime.timedelta(days=7)

        recommended = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]

        context_data.update(recommended=recommended, is_new=is_new)
        return context_data


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
