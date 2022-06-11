# Generated by Django 3.2.5 on 2021-07-12 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0021_rename_pharmacy_orders_pharmacyord'),
    ]

    operations = [
        migrations.CreateModel(
            name='reqPharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharmacy', models.CharField(max_length=30)),
                ('tablet', models.CharField(max_length=30)),
                ('dosage', models.CharField(max_length=30)),
                ('pharmacy_kousi', models.BooleanField(default=False)),
                ('pharmacy_peter', models.BooleanField(default=False)),
                ('Pharmacy_kumar', models.BooleanField(default=False)),
            ],
        ),
    ]
