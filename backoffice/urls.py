from django.urls import path

from .views import backoffice, add_product, edit_product
from .apps import BackofficeConfig

app_name = BackofficeConfig.name

urlpatterns = [
    path("", backoffice, name='backoffice'),
    path("add-product/", add_product, name='add_product'),
    path("edit/<int:product_pk>", edit_product, name='edit_product'),
]
