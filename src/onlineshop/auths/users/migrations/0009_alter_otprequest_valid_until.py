# Generated by Django 4.2.7 on 2023-11-23 08:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_otprequest_valid_until_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='valid_until',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 11, 23, 8, 10, 52, 559467, tzinfo=datetime.timezone.utc)),
        ),
    ]
