# Generated by Django 3.1 on 2020-09-27 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200918_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ban_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
