# Generated by Django 4.2.7 on 2023-11-14 12:47

import datetime
from django.db import migrations, models
import onlineshop.utils.db.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_otprequest_alter_myuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='phone_number',
            field=models.PositiveBigIntegerField(blank=True, error_messages={'unique': 'A user with this mobile number already exists.'}, null=True, unique=True, validators=[onlineshop.utils.db.validators.PhoneNumberValidator()], verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='otprequest',
            name='valid_until',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 11, 14, 12, 49, 37, 987692, tzinfo=datetime.timezone.utc)),
        ),
    ]