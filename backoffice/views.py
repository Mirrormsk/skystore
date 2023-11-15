from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.db import transaction
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from blog.models import Article
from catalog.models import Product, Category, Version
from .forms import (
    ProductForm,
    VersionFormSet,
    ModeratorProductForm,
    SuperuserProductForm,
)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product

    form_class = ProductForm

    success_url = reverse_lazy("backoffice:backoffice")

    extra_context = {
        "title": "Создать новый продукт",
        "categories": Category.objects.all(),
    }

    def form_valid(self, form):
        product = form.save()
        product.producer = self.request.user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product

    success_url = reverse_lazy("backoffice:backoffice")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if self.object.producer != user and not user.has_perm("catalog.can_moderate"):
            raise Http404
        return self.object

    def get_form_class(self):
        user = self.request.user

        if user.has_perm("catalog.set_active") and not user.is_superuser:
            form_class = ModeratorProductForm
        elif user.is_superuser:
            form_class = SuperuserProductForm
        else:
            form_class = ProductForm
        return form_class

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        categories = Category.objects.all()

        if self.request.method == "POST":
            formset = VersionFormSet(self.request.POST, instance=self.object)
        else:
            formset = VersionFormSet(instance=self.object)

        context_data["formset"] = formset
        context_data["categories"] = categories
        context_data["title"] = f"Редактирование товара {product.name}"

        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]

        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()
                if formset.is_valid():

                    formset.instance = self.object
                    formset.save()

                    selected_version_pk = self.request.POST.get("is_selected")
                    selected_version_pk_list = map(
                        str, list(Version.objects.values_list(flat=True))
                    )

                    if selected_version_pk in selected_version_pk_list:

                        selected_version = Version.objects.get(pk=selected_version_pk)
                        formset.instance.version_set.update(is_active=False)
                        selected_version.is_active = True
                        selected_version.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("backoffice:backoffice")
    extra_context = {"title": "Удаление товара"}


@login_required
@permission_required("catalog.set_active")
def toggle_product_activity(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    product_item.is_active = not product_item.is_active
    product_item.save()

    return redirect(reverse_lazy("backoffice:backoffice"))


def toggle_article_activity(request, pk):
    article_item = get_object_or_404(Article, pk=pk)
    article_item.is_published = not article_item.is_published
    article_item.save()

    return redirect(reverse_lazy("backoffice:blog_list"))


class BackofficeProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "backoffice/backoffice_products.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["categories"] = Category.objects.all()
        context_data["title"] = "Товары"
        context_data["nbar"] = "backoffice"
        context_data["selected_category_pk"] = int(self.request.POST.get("category", 0))

        return context_data

    def get_queryset(self):
        user = self.request.user

        category_pk = self.request.POST.get("category", 0)
        categories_pk_list = list(Category.objects.values_list("pk", flat=True))

        if int(category_pk) in categories_pk_list:
            queryset = self.model.objects.filter(category_id=category_pk)
        else:
            queryset = self.model.objects.all()

        if not (user.is_superuser or user.has_perm("catalog.can_moderate")):
            queryset = queryset.filter(producer=user)

        return queryset

    def post(self, request):
        return self.get(request)


class BackofficeArticleListView(LoginRequiredMixin, ListView):
    model = Article

    template_name = "backoffice/backoffice_articles.html"
    extra_context = {"title": "Статьи", "nbar": "backoffice"}


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("backoffice:blog_list")

    extra_context = {"title": "Удаление статьи"}
