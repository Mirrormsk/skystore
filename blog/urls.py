from django.urls import path

from .apps import BlogConfig
from .views import ArticleListView, ArticleCreateView, ArticleUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path("", ArticleListView.as_view(), name='blog_list'),
    path("create/", ArticleCreateView.as_view(), name='article_create'),
    path("edit/<int:pk>", ArticleUpdateView.as_view(), name='article_edit'),
]
