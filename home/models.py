from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone = models.PositiveBigIntegerField(default=0)
    address = models.TextField(default="address")
    city = models.CharField(max_length=100, default="city")
    state = models.CharField(max_length=100, default="state")
    zip = models.CharField(max_length=10,default="0000")
    country = models.CharField(max_length=100,default="country")


class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="merchant")
    name = models.CharField(max_length=100)
    description = models.TextField()
    pet = models.CharField(max_length=100,choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('reptile', 'Reptile'),
        ('small_pet', 'Small Pet'),
        ('other', 'Other')
    ] )
    category = models.CharField(max_length=200,choices=[
        ('food', 'Food'),
        ('toys', 'Toys'),
        ('accessories', 'Accessories'),
        ('grooming', 'Grooming'),
        ('health', 'Health'),
        ('habitat', 'Habitat')
    ] )
    image  = models.FileField(upload_to="product_image")
    price = models.FloatField()
    stock = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_item = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    status = models.CharField(max_length=200, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
        ], default="pending")
    payment_status = models.BooleanField(default=True)
    completion_status = models.BooleanField(default=False)


class BookAppointment(models.Model):
    hospital = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hospital")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient")
    booking_date = models.DateTimeField(auto_now_add=False)
    booked_date = models.DateField(auto_now_add=True)
    pet = models.CharField(max_length=100,choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('reptile', 'Reptile'),
        ('small_pet', 'Small Pet'),
        ('other', 'Other')
        ] )
    treatment = models.CharField(max_length=255, choices=[
        ('vaccination', 'Vaccination'),
        ('checkup', 'Checkup'),
        ('surgery', 'Surgery'),
        ('dental', 'Dental'),
        ('emergency', 'Emergency'),
        ('Grooming',"Grooming"),
        ('other', 'Other')
        ])
    status = models.BooleanField(default=True)

class Vaccinations(models.Model):
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    vaccine_type = models.CharField(max_length=20)
    dosage = models.CharField(max_length=20)
    stock = models.IntegerField()
    pet = models.CharField(max_length=100,choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('reptile', 'Reptile'),
        ('small_pet', 'Small Pet'),
        ('other', 'Other')
        ] )
    age = models.CharField(max_length=20)
    hospital = models.ForeignKey(User,on_delete=models.CASCADE, related_name="vaccine_hospital")




class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    pet_type = models.CharField(max_length=100, choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('reptile', 'Reptile'),
        ('small_pet', 'Small Pet'),
        ('other', 'Other')
    ])
    image = models.ImageField(upload_to="pet_images")

    def __str__(self):
        return self.name


