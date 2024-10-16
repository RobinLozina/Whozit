# Generated by Django 5.1.2 on 2024-10-16 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameLogic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='characters/')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_code', models.CharField(max_length=50, unique=True)),
                ('creator', models.CharField(max_length=50)),
                ('selected_folder', models.CharField(max_length=100)),
            ],
        ),
    ]
