# Generated by Django 5.1.5 on 2025-02-01 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0006_remove_user_is_checked_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_checked_in',
            field=models.BooleanField(default=False),
        ),
    ]
