from django.core.management import BaseCommand, call_command
from django.db import models, transaction

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def delete_everything(model: models.Model) -> None:
        """Delete all objects from model"""
        model.objects.all().delete()

    @transaction.atomic()
    def handle(self, *args, **options):

        # Clear tables
        for model in (Category, Product):
            self.delete_everything(model)

        call_command('loaddata', 'catalog_data.json')
