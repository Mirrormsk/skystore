from django.urls import path

from .apps import BlogConfig
from .views import ArticleListView, ArticleCreateView

app_name = BlogConfig.name

urlpatterns = [
    path("", ArticleListView.as_view(), name='blog_list'),
    path("create/", ArticleCreateView.as_view(), name='article_create'),
]
