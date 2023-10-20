from django.contrib import admin
from django.urls import path

from .views import index, contacts, product, management, add_product

app_name = 'catalog'

urlpatterns = [
    path("", index, name='index'),
    path("contacts/", contacts, name='contacts'),
    path("product/<int:pk>/", product, name='product'),
    path("management/", management, name='management'),
    path("management/add-product/", add_product, name='add_product'),
]
