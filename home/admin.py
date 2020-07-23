from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.TicketStatus)
admin.site.register(models.Berth)
admin.site.register(models.Passengers)
admin.site.register(models.Reservation)