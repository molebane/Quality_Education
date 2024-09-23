# Generated by Django 5.1.1 on 2024-09-23 20:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="school",
            name="location",
            field=models.CharField(
                choices=[("Rural", "Rural"), ("Urban", "Urban")],
                default=django.utils.timezone.now,
                max_length=5,
            ),
            preserve_default=False,
        ),
    ]
