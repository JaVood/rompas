# Generated by Django 2.2.2 on 2020-04-06 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rompas', '0025_auto_20200406_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default='loh', max_length=50, verbose_name='Name'),
        ),
    ]
