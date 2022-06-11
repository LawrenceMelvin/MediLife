# Generated by Django 3.2.5 on 2021-07-09 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='patient_id',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
