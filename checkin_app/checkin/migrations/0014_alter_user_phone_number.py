# Generated by Django 5.1.5 on 2025-02-26 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0013_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
