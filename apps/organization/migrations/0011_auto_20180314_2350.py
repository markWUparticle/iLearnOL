# Generated by Django 2.0.3 on 2018-03-14 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_teacher_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorg',
            name='adress',
        ),
        migrations.AddField(
            model_name='courseorg',
            name='address',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='所在地址'),
        ),
    ]
