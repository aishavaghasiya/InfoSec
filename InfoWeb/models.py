from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class contactUs(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name


class UserProfile1(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
        ('org', 'Organization')
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
