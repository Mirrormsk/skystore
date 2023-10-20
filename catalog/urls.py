from django.contrib import admin
from django.urls import path

from .views import index, contacts, product, management

app_name = 'catalog'

urlpatterns = [
    path("", index, name='index'),
    path("contacts/", contacts, name='contacts'),
    path("product/<int:pk>/", product, name='product'),
    path("management/", management, name='management'),
]
