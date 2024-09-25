# Generated by Django 4.2 on 2024-09-25 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tournament", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tournament",
            name="end_date",
            field=models.DateTimeField(verbose_name="Data de término"),
        ),
        migrations.AlterField(
            model_name="tournament",
            name="start_date",
            field=models.DateTimeField(verbose_name="Data de início"),
        ),
    ]
