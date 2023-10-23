from django.urls import path

from .views import backoffice, ProductCreateView, ProductUpdateView
from .apps import BackofficeConfig

app_name = BackofficeConfig.name

urlpatterns = [
    path("", backoffice, name='backoffice'),
    path("create/", ProductCreateView.as_view(), name='create'),
    path("edit/<int:pk>", ProductUpdateView.as_view(), name='edit_product'),
]
