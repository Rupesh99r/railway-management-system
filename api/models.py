from django.contrib.auth.models import User
from django.db import models

class Train(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    available_seats = models.IntegerField()
    arrival_time_at_source = models.TimeField()
    arrival_time_at_destination = models.TimeField()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

