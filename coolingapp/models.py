from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    agency = models.CharField(default="")
    phone = models.CharField(max_length=10, default="")
    job_positions = models.CharField(max_length=100, default="")
    employee_id = models.CharField(max_length=100, default="")
    profile_picture = models.BinaryField(blank=True, null=True)
    user = models.OneToOneField("coolingapp.CustomUser", on_delete=models.CASCADE)