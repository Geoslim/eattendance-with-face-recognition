# Generated by Django 3.1 on 2020-09-18 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20200918_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='title',
            field=models.CharField(blank=True, max_length=110),
        ),
    ]
