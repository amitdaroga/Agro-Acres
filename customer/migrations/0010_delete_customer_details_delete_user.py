# Generated by Django 4.0 on 2022-01-11 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0010_remove_product_far_id_delete_farmer_details_and_more'),
        ('agroshop', '0033_remove_agroproduct_agro_id_delete_agro_details_and_more'),
        ('nursery', '0007_remove_nursery_details_user_id_delete_nurproduct_and_more'),
        ('customer', '0009_customer_details'),
    ]

    operations = [
        migrations.DeleteModel(
            name='customer_details',
        ),
        migrations.DeleteModel(
            name='user',
        ),
    ]