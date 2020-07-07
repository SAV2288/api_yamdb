from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLES = (('user', ('user')), ('moderator', ('moderator')), ('admin', ('admin')), ('django admin', ('django admin')))


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=30, choices=ROLES, default='user')
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, null=True, default="",unique=True)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Confirmation_code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
