# Generated by Django 3.0.8 on 2020-07-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200724_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='berth',
            name='rac_count',
            field=models.PositiveSmallIntegerField(default=2),
        ),
    ]
