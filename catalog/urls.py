from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ProductListView, ProductDetailView, ContactsTemplateView
from .apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name='index'),
    path("contacts/", cache_page(60)(ContactsTemplateView.as_view()), name='contacts'),
    path("product/<int:pk>/", ProductDetailView.as_view(), name='product'),
]
