# Generated by Django 2.2.2 on 2020-05-21 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rompas', '0033_tokens_name_ru'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='tokens_end',
        ),
    ]
