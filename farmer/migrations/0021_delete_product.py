# Generated by Django 4.0 on 2022-01-22 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0020_remove_product_far_id_product_user_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='product',
        ),
    ]