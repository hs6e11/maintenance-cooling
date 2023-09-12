from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Profile(models.Model):
    address = models.TextField(default="")
    phone = models.CharField(max_length=10, default="")
    job_positions = models.CharField(max_length=100, default="")
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    user = models.OneToOneField("coolingapp.CustomUser", on_delete=models.CASCADE)