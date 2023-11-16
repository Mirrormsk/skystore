from django.db import models
from catalog.models import TimeStampedModel

from catalog.models import NULLABLE


class Article(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.CharField(max_length=255, verbose_name='Slug', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name='автор', **NULLABLE)

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['-created_at']

    def __str__(self):
        if len(self.title) <= 50:
            return self.title
        return f"{self.title[:50]}..."
