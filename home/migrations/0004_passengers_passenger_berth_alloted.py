# Generated by Django 3.0.8 on 2020-07-24 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='passengers',
            name='passenger_berth_alloted',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Berth'),
        ),
    ]
