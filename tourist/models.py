from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user.username
    
class Destination(models.Model):
    place_name = models.CharField(max_length=100)
    weather = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    google_map_link = models.URLField()
    description = models.TextField()
   

    def __str__(self):
        return self.place_name