# Generated by Django 4.2.7 on 2023-11-16 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_alter_user_account_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="account_balance",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]