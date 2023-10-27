# Generated by Django 4.2.6 on 2023-10-27 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_alter_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("ANALYST", "Analyst"), ("USER", "User"), ("ADMIN", "Admin")],
                default="User",
                max_length=10,
                verbose_name="Role",
            ),
        ),
    ]
