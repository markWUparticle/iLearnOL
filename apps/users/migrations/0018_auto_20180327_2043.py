# Generated by Django 2.0.3 on 2018-03-27 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20180315_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '忘记密码'), ('update_eamil', '修改邮箱')], max_length=50, verbose_name='验证类型'),
        ),
    ]
