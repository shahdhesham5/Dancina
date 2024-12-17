# Generated by Django 4.2.16 on 2024-12-11 07:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0013_package_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiolocation',
            name='share_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
