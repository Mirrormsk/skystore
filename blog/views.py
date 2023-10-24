from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .models import Article


class ArticleListView(ListView):
    model = Article


class ArticleCreateView(CreateView):
    model = Article

    fields = (
        'title',
        'slug',
        'content',
        'preview',
        'is_published'
    )

    success_url = reverse_lazy('blog:blog_list')


class ArticleUpdateView(UpdateView):
    model = Article

    fields = (
        'title',
        'slug',
        'content',
        'preview',
        'is_published'
    )

    success_url = reverse_lazy('blog:blog_list')
