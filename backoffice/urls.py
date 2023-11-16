from django.urls import path
from django.views.decorators.cache import never_cache

from .apps import BackofficeConfig
from .views import (
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    toggle_product_activity,
    BackofficeProductListView,
    BackofficeArticleListView,
    ArticleDeleteView,
    toggle_article_activity,
)

app_name = BackofficeConfig.name

urlpatterns = [
    path("", never_cache(BackofficeProductListView.as_view()), name='backoffice'),
    path("products/", never_cache(BackofficeProductListView.as_view()), name='backoffice_products'),
    path("create/", never_cache(ProductCreateView.as_view()), name='create'),
    path("edit/<int:pk>", never_cache(ProductUpdateView.as_view()), name='edit_product'),
    path("product/delete/<int:pk>", never_cache(ProductDeleteView.as_view()), name='delete_product'),
    path("product/activity/<int:pk>", never_cache(toggle_product_activity), name='toggle_product_activity'),
    path("article/activity/<int:pk>", never_cache(toggle_article_activity), name='toggle_article_activity'),
    path("article/delete/<int:pk>", never_cache(ArticleDeleteView.as_view()), name='delete_article'),
    path("blog/", never_cache(BackofficeArticleListView.as_view()), name='blog_list'),
]
