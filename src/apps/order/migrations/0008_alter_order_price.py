# Generated by Django 4.2.6 on 2023-10-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0007_alter_order_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="price",
            field=models.DecimalField(
                decimal_places=6,
                default=None,
                max_digits=12,
                null=True,
                verbose_name="Price",
            ),
        ),
    ]
