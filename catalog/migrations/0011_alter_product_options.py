# Generated by Django 4.2.6 on 2023-11-15 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0010_alter_product_is_active"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["-pk"],
                "permissions": [
                    ("set_active", "Can set active"),
                    ("can_moderate", "Can moderate"),
                ],
                "verbose_name": "продукт",
                "verbose_name_plural": "продукты",
            },
        ),
    ]