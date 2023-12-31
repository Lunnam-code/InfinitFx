# Generated by Django 4.2.6 on 2023-10-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_user_is_superadmin_alter_user_is_superuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="account_balance",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(blank=True, upload_to="images/users/"),
        ),
    ]
