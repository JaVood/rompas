# Generated by Django 2.2.2 on 2019-08-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rompas', '0015_auto_20190806_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_buy',
            field=models.BooleanField(default=False, verbose_name='Can buy'),
        ),
    ]
