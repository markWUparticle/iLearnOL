# Generated by Django 2.0.3 on 2018-03-11 19:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20180311_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='add_time',
            field=models.DateField(default=datetime.datetime.now, verbose_name='注册时间'),
        ),
    ]
