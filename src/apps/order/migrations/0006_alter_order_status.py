# Generated by Django 4.2.6 on 2023-10-27 13:21

from django.db import migrations, models

import apps.base.enums


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0005_alter_order_status_alter_order_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("IN_PROGRESS", "In Progress"),
                    ("DONE", "Done"),
                    ("CANCELED", "Canceled"),
                ],
                default=apps.base.enums.OrderStatus["IN_PROGRESS"],
                max_length=15,
                verbose_name="Status",
            ),
        ),
    ]
