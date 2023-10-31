# Generated by Django 4.2.6 on 2023-10-28 22:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0006_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="price",
            field=models.DecimalField(
                decimal_places=6,
                default=0,
                max_digits=12,
                null=True,
                verbose_name="Price",
            ),
        ),
    ]