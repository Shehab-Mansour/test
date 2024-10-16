from django.db import models
from unicodedata import numeric
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class users(models.Model):
    username = models.CharField(max_length=50 , null=False)
    password = models.CharField(max_length=500,null=False)
    email = models.CharField(max_length=50 , null=False)
    birthday = models.DateField(null=False)
    state = models.BooleanField(default=False)
    def __str__(self):
        return self.username




class CustomToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey('users', related_name='auth_tokens', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
