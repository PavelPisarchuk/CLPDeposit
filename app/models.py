from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    father_name = models.CharField(max_length=30)
    passport_id = models.CharField(max_length=14)

    def get_full_name(self):
        return self.username if self.is_superuser else "{} {} {}".format(self.last_name, self.first_name, self.father_name)

    def get_short_name(self):
        return self.username if self.is_superuser else "{} {}. {}.".format(self.last_name, self.first_name[0], self.father_name[0])


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
