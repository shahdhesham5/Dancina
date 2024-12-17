# Generated by Django 4.2.16 on 2024-12-12 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_remove_registration_expiration_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='expiration_date',
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
