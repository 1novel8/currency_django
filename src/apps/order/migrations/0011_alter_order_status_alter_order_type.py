# Generated by Django 4.2.6 on 2023-10-30 14:56

from django.db import migrations, models

import apps.base.enums


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0010_alter_order_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("In Progress", "In Progress"),
                    ("Done", "Done"),
                    ("Canceled", "Canceled"),
                ],
                default=apps.base.enums.OrderStatus["IN_PROGRESS"],
                max_length=15,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="type",
            field=models.CharField(
                choices=[("Buy", "Buy"), ("Sale", "Sale")],
                default=apps.base.enums.OrderType["BUY"],
                max_length=10,
                verbose_name="Type",
            ),
        ),
    ]
