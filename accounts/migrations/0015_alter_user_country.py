# Generated by Django 4.2.7 on 2023-11-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0014_alter_user_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="country",
            field=models.CharField(max_length=50),
        ),
    ]
