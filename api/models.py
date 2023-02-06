from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)


