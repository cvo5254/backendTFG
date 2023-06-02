from django.db import models
from users.models import CustomUser

class Channel(models.Model):
    nombre = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(CustomUser)
    is_blocked= models.BooleanField(default=False)
