# Generated by Django 4.2.7 on 2023-11-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_user_pending_commission_user_referral_link_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="account_balance",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
