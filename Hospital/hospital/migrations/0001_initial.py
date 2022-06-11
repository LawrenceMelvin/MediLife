# Generated by Django 3.2.3 on 2021-07-08 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=45)),
                ('message', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('phone', models.BigIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('phone', models.BigIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pharmacy', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('phone', models.BigIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=45)),
            ],
        ),
    ]
