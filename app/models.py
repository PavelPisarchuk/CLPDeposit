from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    father_name = models.CharField(max_length=30)


class Deposit(models.Model):
    pass


class Contract(models.Model):
    pass


class Pay(models.Model):
    pass