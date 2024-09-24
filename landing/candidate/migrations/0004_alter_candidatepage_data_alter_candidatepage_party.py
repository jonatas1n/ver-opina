# Generated by Django 4.2 on 2024-09-24 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("candidate", "0003_party_alter_candidatepage_party"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidatepage",
            name="data",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="candidatepage",
            name="party",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="candidate.party",
            ),
        ),
    ]
