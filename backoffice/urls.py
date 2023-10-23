from django.urls import path

from .views import backoffice, ProductCreateView, ProductUpdateView, ProductDeleteView, toggle_product_activity
from .apps import BackofficeConfig

app_name = BackofficeConfig.name

urlpatterns = [
    path("", backoffice, name='backoffice'),
    path("create/", ProductCreateView.as_view(), name='create'),
    path("edit/<int:pk>", ProductUpdateView.as_view(), name='edit_product'),
    path("delete/<int:pk>", ProductDeleteView.as_view(), name='delete_product'),
    path("activity/<int:pk>", toggle_product_activity, name='toggle_activity'),
]
