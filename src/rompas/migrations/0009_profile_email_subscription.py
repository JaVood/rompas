# Generated by Django 2.2.2 on 2019-08-01 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rompas', '0008_profile_tokens_left'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_subscription',
            field=models.BooleanField(default=True, verbose_name='Email subscription'),
        ),
    ]