# Generated by Django 2.0.3 on 2018-03-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0016_auto_20180316_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='全国知名', max_length=10, verbose_name='机构标签'),
        ),
    ]
