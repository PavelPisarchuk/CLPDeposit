from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    father_name = models.CharField(max_length=30)


class Deposit(models.Model):
    percent = models.IntegerField()
    pay_period = models.IntegerField()
    interval = models.IntegerField()


class Contract(models.Model):
    client = models.ForeignKey(User)
    deposit = models.ForeignKey(Deposit)
    signed = models.DateTimeField()


class Pay(models.Model):
    contract = models.ForeignKey(Contract)


class Bill(models.Model):
    client = models.ForeignKey(User)
