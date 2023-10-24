from django.core.management import BaseCommand, call_command
from django.db import models, transaction


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('loaddata', 'blog_data.json')
