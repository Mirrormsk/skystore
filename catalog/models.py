from django.db import models
from django.utils import timezone

# Nullable parameters
NULLABLE = {"null": True, "blank": True}


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides
    self-updating 'created_at' and 'updated_at' field
    """
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Изменен')

    class Meta:
        abstract = True


class Category(models.Model):
    """Category model """
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f"{self.name}"


class Product(TimeStampedModel):
    """Product model with timestamp"""
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='catalog/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')

    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['-pk']

    def __str__(self):
        return f"{self.name} ({self.category.name})"





class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')

    class Meta:
        verbose_name = 'организация'
        verbose_name_plural = 'организации'

    def __str__(self):
        return self.name
