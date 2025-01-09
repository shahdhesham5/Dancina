# Generated by Django 4.2.16 on 2025-01-09 12:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calendarapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Phone number must be up to 11 digits and numeric only.', regex='^\\d{1,11}$')])),
                ('preferred_time', models.TextField(blank=True, max_length=500, null=True)),
                ('is_member', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('TOTAL', 'Total Payment'), ('PARTIAL', 'Partial Payment')], max_length=20)),
                ('price_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('price_left', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('classes_attended', models.PositiveIntegerField(default=0)),
                ('classes_left', models.PositiveIntegerField()),
                ('registration_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('expiration_date', models.DateTimeField(db_index=True, null=True)),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='calendarapp.event')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='clients.client')),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendarapp.package')),
                ('package_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calendarapp.packagetype')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_receipt_number', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('VISA', 'Visa'), ('CASH', 'Cash'), ('INSTAPAY', 'Instapay')], max_length=10, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receipt_number', models.PositiveIntegerField(unique=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='clients.client')),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_registration', to='clients.registration')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='classes',
            field=models.ManyToManyField(related_name='clients', through='clients.Registration', to='calendarapp.event'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='clients.client')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='calendarapp.event')),
            ],
        ),
    ]
