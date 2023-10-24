from django.urls import path

from .views import ProductCreateView, ProductUpdateView, ProductDeleteView, toggle_product_activity, \
    BackofficeProductListView, BackofficeArticleListView, toggle_article_activity
from .apps import BackofficeConfig

app_name = BackofficeConfig.name

urlpatterns = [
    path("", BackofficeProductListView.as_view(), name='backoffice'),
    path("products/", BackofficeProductListView.as_view(), name='backoffice_products'),
    path("create/", ProductCreateView.as_view(), name='create'),
    path("edit/<int:pk>", ProductUpdateView.as_view(), name='edit_product'),
    path("delete/<int:pk>", ProductDeleteView.as_view(), name='delete_product'),
    path("product/activity/<int:pk>", toggle_product_activity, name='toggle_product_activity'),
    path("article/activity/<int:pk>", toggle_article_activity, name='toggle_article_activity'),

    path("blog/", BackofficeArticleListView.as_view(), name='blog_list'),
]
