from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .models import Article


class ArticleListView(ListView):
    model = Article

    extra_context = {
        'title': 'SkyStore | Блог',
        'nbar': 'blog'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


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


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
