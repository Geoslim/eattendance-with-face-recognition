# Generated by Django 3.1 on 2020-10-14 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200930_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='lateness_ago',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
