from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

import uuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(130), MinValueValidator(1)])
    gender = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.get_full_name()


class TicketStatus(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4)    
    status_name = models.CharField(max_length=32)

    def __str__(self):
        return self.status_name


class Berth(models.Model):
    berth_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    seat_no = models.PositiveSmallIntegerField()
    seat_name = models.CharField(max_length=6)
    coach_name = models.CharField(max_length=6)    

    def __str__(self):
        return str(self.seat_no) + '_' + self.seat_name + '_' + self.coach_name


class Reservation(models.Model):
    reservation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    reserved_user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_passengers = models.PositiveSmallIntegerField()
    reservation_time = models.DateTimeField(auto_now_add=True)
    ticket_authorized = models.BooleanField(default=True)

    def __str__(self):
        return str(self.reserved_user) + '_' + str(self.reservation_time.strftime('%d-%m-%Y %H:%M:%S'))


class Passengers(models.Model):
    passenger_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    passenger_reservation_id = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=128)
    passenger_age = models.PositiveSmallIntegerField()
    passenger_gender = models.CharField(max_length=10)
    passenger_berth_preference = models.CharField(max_length=3)
    passenger_ticket_status = models.ForeignKey('TicketStatus', on_delete=models.CASCADE)
    passenger_authorized = models.BooleanField(default=True)

    def __str__(self):
        return str(self.passenger_reservation_id) + '_' + str(self.passenger_name)
