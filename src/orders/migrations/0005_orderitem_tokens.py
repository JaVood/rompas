# Generated by Django 2.2.2 on 2020-04-15 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rompas', '0029_tokens'),
        ('orders', '0004_auto_20200415_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='tokens',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_tokens', to='rompas.Tokens'),
        ),
    ]
