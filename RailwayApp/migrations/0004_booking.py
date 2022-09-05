# Generated by Django 4.0 on 2022-03-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RailwayApp', '0003_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('railId', models.CharField(max_length=50)),
                ('railName', models.CharField(max_length=100)),
                ('fromAddress', models.CharField(max_length=100)),
                ('toAddress', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('userId', models.CharField(max_length=50)),
                ('fullname', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'booking',
            },
        ),
    ]