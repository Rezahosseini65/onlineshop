# Generated by Django 4.2.7 on 2023-12-07 13:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_otprequest_valid_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='valid_until',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 12, 7, 13, 3, 23, 465132, tzinfo=datetime.timezone.utc)),
        ),
    ]
