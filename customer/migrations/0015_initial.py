# Generated by Django 4.0 on 2022-01-22 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0014_delete_customer_details_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('otp', models.IntegerField(default=7812)),
            ],
        ),
        migrations.CreateModel(
            name='customer_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(default='media/profile/default.png', upload_to='media/profile')),
                ('dod', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('pincode', models.CharField(max_length=100, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.user')),
            ],
        ),
    ]