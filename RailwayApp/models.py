from django.db import models

class AdminLogin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    class Meta:
        db_table = "admin_login"


class Rail(models.Model):
    name = models.CharField(max_length=100)
    fromAddress = models.CharField(max_length=100)
    toAddress = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    date = models.DateField(null=False, blank=False)
    time = models.CharField(max_length=50)

    class Meta:
        db_table = "rail"


class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    image_url = models.FileField(upload_to='images')
    verified = models.BooleanField(null=True, default = False)

    class Meta:
        db_table = "users"


class Booking(models.Model):
    railId = models.CharField(max_length=50, null=True)
    railName = models.CharField(max_length=100, null=True)
    fromAddress = models.CharField(max_length=100, null=True)
    toAddress = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    userId = models.CharField(max_length=50, null=True)
    fullname = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=50, null=True)
    accept = models.BooleanField(null=True)
    date = models.DateField(null=True)

    class Meta:
        db_table = "booking"


class Seat(models.Model):
    railId = models.CharField(max_length=50)
    userId = models.CharField(max_length=50)
    seatNumber = models.CharField(max_length=50)
    date = models.DateField(null=False, blank=False)

    class Meta:
        db_table = "seat"
