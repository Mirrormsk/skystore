import datetime

from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView

from .models import Product, Organization
from .services import messages_saver


class ProductListView(ListView):
    model = Product
    paginate_by = 5

    extra_context = {
        'title': 'SkyStore - Главная',
        'nbar': 'home',
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)

        return queryset


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        product = Product.objects.get(pk=self.kwargs.get('pk'))
        is_new = timezone.now() - product.created_at <= datetime.timedelta(days=7)

        recommended = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]

        context_data['recommended'] = recommended
        context_data['is_new'] = is_new
        context_data['title'] = product.name

        return context_data


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    extra_context = {
        'nbar': 'contacts',
        'title': 'Контакты',
        'organization': Organization.objects.get(pk=1)
    }

    def post(self, *args):
        messages_saver.save_message(self.request.POST)
        messages.info(self.request, 'Ваше сообщение принято и будет обработано')
        return self.get(self.request)
