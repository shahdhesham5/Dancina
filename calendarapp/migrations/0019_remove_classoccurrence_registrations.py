# Generated by Django 4.2.16 on 2024-12-16 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0018_event_is_private_eventmember_is_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classoccurrence',
            name='registrations',
        ),
    ]
