# Generated by Django 4.2.16 on 2024-11-26 08:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0008_alter_package_package_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instructor',
            name='share_percentage',
        ),
        migrations.AddField(
            model_name='instructor',
            name='share_percentage_group',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='instructor',
            name='share_percentage_private',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
