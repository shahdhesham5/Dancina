# Generated by Django 4.2.16 on 2024-11-25 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0007_packagetype_package_package_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='package_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_type', to='calendarapp.packagetype'),
        ),
    ]
