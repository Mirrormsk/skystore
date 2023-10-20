from django.urls import path

from .views import management, add_product
from .apps import BackofficeConfig

app_name = BackofficeConfig.name

urlpatterns = [
    path("", management, name='backoffice'),
    path("add-product/", add_product, name='add_product'),
]
