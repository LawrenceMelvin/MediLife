# Generated by Django 3.2.5 on 2021-07-10 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0008_lab'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab_report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(default=None, max_length=20)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
                ('phone', models.BigIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=255)),
                ('speciality', models.CharField(max_length=30)),
                ('doctors', models.CharField(max_length=30)),
                ('date', models.CharField(max_length=30)),
                ('time', models.CharField(max_length=30)),
                ('symptoms', models.CharField(max_length=30)),
                ('problems', models.CharField(max_length=30)),
                ('report_boolean', models.BooleanField(default=False)),
                ('report', models.FileField(default=None, upload_to='media/')),
                ('age', models.IntegerField()),
                ('prescription_boolean', models.BooleanField(default=False)),
                ('prescription', models.FileField(default=None, upload_to='media/')),
            ],
        ),
    ]
