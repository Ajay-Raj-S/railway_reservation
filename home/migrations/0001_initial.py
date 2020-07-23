# Generated by Django 3.0.8 on 2020-07-23 15:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Berth',
            fields=[
                ('berth_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('seat_no', models.PositiveSmallIntegerField()),
                ('seat_name', models.CharField(max_length=6)),
                ('coach_name', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(130), django.core.validators.MinValueValidator(1)])),
                ('gender', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
