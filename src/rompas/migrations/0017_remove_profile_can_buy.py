# Generated by Django 2.2.2 on 2019-08-08 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rompas', '0016_profile_can_buy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='can_buy',
        ),
    ]
