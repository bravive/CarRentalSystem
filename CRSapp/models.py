from django.db import models
# Create your models here.
from django.contrib.auth.models import User
# Register your models here.

class CarType(models.Model):
    cartype = models.CharField(max_length=200)
    rentalfee = models.PositiveIntegerField(max_length=200)
    picture = models.ImageField(upload_to="Car-type-picture")
    createdtime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.cartype

class CarInventory(models.Model):
    CIN = models.CharField(max_length=200)
    cartype = models.ForeignKey(CarType)
    mile = models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    createdtime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.CIN
class CarReserveTimeSheet(models.Model):
    car = models.ForeignKey(CarInventory)
    fromdate = models.CharField(max_length=200)
    fromtime = models.CharField(max_length=200)
    todate = models.CharField(max_length=200)
    totime = models.CharField(max_length=200)
    def __unicode__(self):
        return self.car.CIN
class UserReserveHistory(models.Model):
    user = models.ForeignKey(User)
    status_reserved = models.BooleanField(default=False)
    status_deleted = models.BooleanField(default=False)
    status_confirmed = models.BooleanField(default=False)
    status_returned = models.BooleanField(default=False)
    CIN = models.CharField(max_length=200)
    fromdate = models.CharField(max_length=200)
    fromtime = models.CharField(max_length=200)
    todate = models.CharField(max_length=200)
    totime = models.CharField(max_length=200)
    createdtime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.user.username
class Profile(models.Model):
    owner = models.OneToOneField(User)
    First_name = models.CharField(max_length=200, default="", blank=True)
    Last_name = models.CharField(max_length=200, default="", blank=True)
    Address_1 = models.CharField(max_length=200, default="", blank=True)
    Address_2 = models.CharField(max_length=200, default="", blank=True)
    City = models.CharField(max_length=200, default="", blank=True)
    State = models.CharField(max_length=200, default="", blank=True)
    Zip = models.CharField(max_length=6, default="", blank=True)
    Country = models.CharField(max_length=200, default="", blank=True)
    Phone = models.CharField(max_length=15, default="",blank=True)
    picture = models.ImageField(upload_to="profile-photos", blank=True)
    def __unicode__(self):
        return self.owner
