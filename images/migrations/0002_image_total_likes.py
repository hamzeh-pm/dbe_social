# Generated by Django 4.1 on 2022-08-21 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="total_likes",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
