from django.core.management import BaseCommand
from django.db import models

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def delete_everything(self, model: models.Model) -> None:
        """Delete all objects from model"""
        model.objects.all().delete()

    def handle(self, *args, **options):
        pass
