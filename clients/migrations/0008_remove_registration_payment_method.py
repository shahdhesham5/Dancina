# Generated by Django 4.2.16 on 2024-12-11 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_transaction_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='payment_method',
        ),
    ]