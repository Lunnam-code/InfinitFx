# Generated by Django 4.2.6 on 2023-10-06 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_rename_image_user_profile_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="agree_to_terms_and_condition",
            field=models.BooleanField(default=False),
        ),
    ]