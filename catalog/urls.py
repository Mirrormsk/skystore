from django.urls import path

from .views import ProductListView, ProductDetailView, ContactsTemplateView

app_name = 'catalog'

urlpatterns = [
    path("", ProductListView.as_view(), name='index'),
    path("contacts/", ContactsTemplateView.as_view(), name='contacts'),
    path("product/<int:pk>/", ProductDetailView.as_view(), name='product'),
]
