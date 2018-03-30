# Generated by Django 2.0.3 on 2018-03-30 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_auto_20180330_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginbanner',
            name='image',
            field=models.ImageField(blank=True, max_length=50, null=True, upload_to='banner/%Y/%m', verbose_name='轮播图'),
        ),
        migrations.AlterField(
            model_name='loginbanner',
            name='index',
            field=models.IntegerField(default=1, verbose_name='顺序'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(default='还没想好名字', max_length=50, verbose_name='昵称'),
        ),
    ]
