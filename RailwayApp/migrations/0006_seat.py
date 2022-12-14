# Generated by Django 4.0 on 2022-03-23 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RailwayApp', '0005_booking_accept_alter_booking_contact_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('railId', models.CharField(max_length=50)),
                ('userId', models.CharField(max_length=50)),
                ('seatNumber', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
            options={
                'db_table': 'seat',
            },
        ),
    ]
