# Generated by Django 2.2.2 on 2019-07-31 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rompas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rompas.Subscription', verbose_name='Subscription'),
        ),
    ]