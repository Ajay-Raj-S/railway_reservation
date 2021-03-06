# Generated by Django 3.0.8 on 2020-07-24 03:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_passengers_reservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('total_tickets', models.PositiveSmallIntegerField()),
                ('cnf_tickets', models.PositiveSmallIntegerField()),
                ('rac_tickets', models.PositiveSmallIntegerField()),
                ('waiting_tickets', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
