# Generated by Django 3.2.5 on 2021-07-12 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0017_auto_20210712_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacy_orders',
            name='doctor',
            field=models.CharField(default='', max_length=30),
        ),
    ]
