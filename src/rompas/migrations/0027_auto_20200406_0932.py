# Generated by Django 2.2.2 on 2020-04-06 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rompas', '0026_auto_20200406_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]