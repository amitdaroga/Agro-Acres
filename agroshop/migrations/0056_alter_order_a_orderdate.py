# Generated by Django 4.0 on 2022-01-31 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroshop', '0055_order_a_orderdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_a',
            name='orderdate',
            field=models.DateField(auto_now=True),
        ),
    ]