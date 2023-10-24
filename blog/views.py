from django.urls import reverse_lazy, reverse
from smtplib import SMTPDataError
from config.settings import EMAIL_ADMIN, DEFAULT_FROM_EMAIL

from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from pytils.translit import slugify

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

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article

    fields = (
        'title',
        'slug',
        'content',
        'preview',
        'is_published'
    )

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1

        views_notification_count = 100

        if self.object.views_count == views_notification_count:
            subject = 'SkyStore - статья пользуется популярностью!'
            body = f'Ваша статья "{self.object.title}" набрала {views_notification_count} просмотров!'
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [EMAIL_ADMIN, 'm.donchuk@gmail.com']

            try:
                send_mail(subject, body, from_email=from_email, recipient_list=recipient_list)
            except SMTPDataError as ex:
                print(f'Ошибка отправки письма:\n{ex}')

        self.object.save()
        return self.object
