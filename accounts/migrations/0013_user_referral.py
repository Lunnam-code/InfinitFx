# Generated by Django 4.2.7 on 2023-11-17 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("referral_system", "0001_initial"),
        ("accounts", "0012_alter_user_account_balance"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="referral",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="referral_system.referral",
            ),
        ),
    ]