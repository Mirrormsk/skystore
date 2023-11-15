# Generated by Django 4.2.6 on 2023-11-12 17:34

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_country_user_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="country",
            field=django_countries.fields.CountryField(
                blank=True, max_length=2, null=True, verbose_name="Страна"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="активен"),
        ),
    ]