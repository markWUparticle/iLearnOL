# Generated by Django 2.0.3 on 2018-03-11 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180311_1521'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EailverifyRecord',
            new_name='EmailVerifyRecord',
        ),
    ]
