# Generated by Django 4.2.6 on 2023-10-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="slug",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Slug"
            ),
        ),
    ]
