from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    birthday = models.DateField(null=True)
    phoneNumber = models.PositiveIntegerField(null=True)
    allergy = models.CharField(max_length=100, blank=True, default="")
    gender = models.CharField(max_length=1, default="o")
    bio = models.CharField(max_length=500, blank=True, default="")


