from django.urls import path

from .views import ProductListView, ProductDetailView, ContactsTemplateView
from .apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name='index'),
    path("contacts/", ContactsTemplateView.as_view(), name='contacts'),
    path("product/<int:pk>/", ProductDetailView.as_view(), name='product'),
]
