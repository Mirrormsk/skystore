import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    country = CountryField(**NULLABLE, verbose_name='Страна')
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False, verbose_name='активен')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

