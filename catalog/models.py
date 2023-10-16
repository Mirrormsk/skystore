from django.db import models

# Create your models here.


NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE)

    def __str__(self):
        return f"Category <{self.name}>"


