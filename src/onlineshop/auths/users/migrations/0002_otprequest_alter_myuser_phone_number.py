# Generated by Django 4.2.7 on 2023-11-14 12:46

import datetime
from django.db import migrations, models
import django.utils.timezone
import onlineshop.utils.db.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPrequest',
            fields=[
                ('request_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('channel', models.CharField(choices=[('web', 'Web'), ('android', 'Android'), ('ios', 'Ios')], default='web', max_length=7, verbose_name='Channel')),
                ('phone', models.CharField(max_length=12, unique=True, verbose_name='Phone Number')),
                ('password', models.CharField(max_length=4, null=True)),
                ('valid_from', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_until', models.DateTimeField(verbose_name=datetime.datetime(2023, 11, 14, 12, 48, 39, 30388, tzinfo=datetime.timezone.utc))),
                ('receive_id', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'One Time Password',
                'verbose_name_plural': 'One Time Passwords ',
            },
        ),
        migrations.AlterField(
            model_name='myuser',
            name='phone_number',
            field=models.PositiveBigIntegerField(blank=True, error_messages={'unique': 'A user with this mobile number already exists.'}, max_length=13, null=True, unique=True, validators=[onlineshop.utils.db.validators.PhoneNumberValidator()], verbose_name='Phone Number'),
        ),
    ]