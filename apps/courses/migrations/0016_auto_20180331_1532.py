# Generated by Django 2.0.3 on 2018-03-31 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_auto_20180330_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='big_image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/%Y/%m', verbose_name='详情大图'),
        ),
    ]
