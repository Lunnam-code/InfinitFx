# Generated by Django 4.2.7 on 2023-11-14 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_user_agree_to_terms_and_condition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="account_balance",
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]