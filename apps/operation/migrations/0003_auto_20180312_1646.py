# Generated by Django 2.0.3 on 2018-03-12 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20180311_1450'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursecomments',
            options={'verbose_name': '用户评论', 'verbose_name_plural': '用户评论'},
        ),
        migrations.AlterModelOptions(
            name='userask',
            options={'verbose_name': '用户咨询', 'verbose_name_plural': '用户咨询'},
        ),
    ]
