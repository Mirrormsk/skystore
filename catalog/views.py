import datetime

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import cache_page, never_cache
from django.views.generic import ListView, DetailView, TemplateView

from .models import Product, Organization
from .services import messages_saver

production_cache = cache_page(60 * 5) if settings.DEBUG else never_cache


class ProductListView(ListView):
    model = Product
    paginate_by = 5

    extra_context = {
        "title": "SkyStore - Главная",
        "nbar": "home",
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)

        return queryset


class ProductDetailView(DetailView):
    model = Product

    def is_user_creator_or_moderator_of(self, product):
        user = self.request.user
        return (
            user.is_authenticated
            and product.producer == user
            or user.is_superuser
            or user.has_perm("catalog.can_moderate")
        )

    def get_object(self, queryset=None):
        product = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        if not product.is_active:
            if not self.is_user_creator_or_moderator_of(product):
                raise Http404
        return product

    def get_context_data(self, **kwargs):
        user = self.request.user
        context_data = super().get_context_data(**kwargs)

        product = Product.objects.get(pk=self.kwargs.get("pk"))
        is_new = timezone.now() - product.created_at <= datetime.timedelta(days=7)

        recommended = Product.objects.filter(category=product.category).exclude(
            pk=product.pk
        )[:3]

        if not product.is_active:
            if self.is_user_creator_or_moderator_of(product):
                context_data["show_not_active_product"] = True

        context_data["recommended"] = recommended
        context_data["is_new"] = is_new
        context_data["title"] = product.name

        return context_data


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    extra_context = {
        "nbar": "contacts",
        "title": "Контакты",
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        organization = Organization.objects.filter(is_active=True).last()
        context_data["organization"] = organization
        return context_data

    def post(self, *args):
        messages_saver.save_message(self.request.POST)
        messages.info(self.request, "Ваше сообщение принято и будет обработано")
        return self.get(self.request)
