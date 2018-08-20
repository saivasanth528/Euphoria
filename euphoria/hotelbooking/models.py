from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
from euphoria.settings import AUTH_USER_MODEL


class Hotel_users(AbstractUser):
    isHotel_representative = models.BooleanField(default=False)


class Customer_details(models.Model):

    Name = models.CharField(max_length=128)
    Age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(65)])
    Mobile_number = models.CharField(max_length = 10)
    Email = models.EmailField()
    proof_id = models.CharField(max_length=30)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.Name

class Booking_details(models.Model):

    hotel_name = models.CharField(max_length=50)
    hotel_id = models.IntegerField(default = 0)
    location = models.CharField(max_length=50)
    booking_instant =  models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    amount = models.IntegerField()
    no_of_rooms = models.IntegerField(default=1)
    Number_of_guests = models.PositiveIntegerField(default=1)
    Special_request = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer_details, on_delete=models.CASCADE)


    def __str__(self):
        return self.hotel_name


hotel_rating_choices  = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
)

class Hotel(models.Model):

    Hotel_Name = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    no_of_rooms = models.IntegerField()
    room_price = models.IntegerField()
    rating = models.CharField(max_length=1, choices=hotel_rating_choices, default=3)
    Hotel_main_image = models.FileField(upload_to='hotel_images/')
    Hotel_images = models.FileField(upload_to='hotel_images', blank=True, null = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.Hotel_Name

class Hotel_image(models.Model):

    hotel_img = models.ImageField(upload_to = 'hotel_images/', blank = True, null = True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_images")

class Hotel_search(models.Model):

    location = models.CharField(max_length=20)
    check_in  = models.DateField()
    check_out = models.DateField()
    adults = models.IntegerField()
    children = models.IntegerField()
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.location

