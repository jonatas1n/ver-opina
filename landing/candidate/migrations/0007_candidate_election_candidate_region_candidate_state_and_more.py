# Generated by Django 4.2 on 2024-09-25 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidate", "0006_rename_candidate_name_candidate_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="election",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Id da Eleição"
            ),
        ),
        migrations.AddField(
            model_name="candidate",
            name="region",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="candidate",
            name="state",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="candidate",
            name="year",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="election_id",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="ID do candidato na Eleição",
            ),
        ),
    ]
