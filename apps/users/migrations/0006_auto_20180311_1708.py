# Generated by Django 2.0.3 on 2018-03-11 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180311_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailverifyrecord',
            old_name='set_type',
            new_name='seend_type',
        ),
    ]
