# Generated by Django 4.2.6 on 2023-11-15 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_product_producer"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["-pk"],
                "permissions": [("set_active", "Can set active")],
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты",
            },
        ),
    ]