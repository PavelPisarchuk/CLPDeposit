from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    father_name = models.CharField(max_length=30)
    passport_id = models.CharField(max_length=14)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)

    def get_full_name(self):
        return self.username if self.is_superuser else "{} {} {}".format(self.last_name, self.first_name, self.father_name)

    def get_short_name(self):
        return self.username if self.is_superuser else "{} {}. {}.".format(self.last_name, self.first_name[:1], self.father_name[:1])


class Deposit(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    percent = models.IntegerField()
    min_storing_term = models.IntegerField()
    max_storing_term = models.IntegerField()
    pay_term = models.IntegerField()
    refill = models.BooleanField()
    partial_take = models.BooleanField()
    indexed = models.BooleanField()
    currency = models.ForeignKey(Currency)


class Contract(models.Model):
    bill = models.ForeignKey(Bill)
    deposit = models.ForeignKey(Deposit)
    sign_date = models.DateTimeField()
    term = models.IntegerField()
    money = models.FloatField()

    def get_storing_term(self):
        from datetime import date
        return (date.today() - self.sign_date).days


class Pay(models.Model):
    agent = models.ForeignKey(User)
    contract = models.ForeignKey(Contract)
    datetime = models.DateTimeField()
    money = models.FloatField()


class Bill(models.Model):
    client = models.ForeignKey(User)
    money = models.FloatField()
    currency = models.ForeignKey(Currency)


class Currency(models.Model):
    title = models.CharField(max_length=2)


class ExchangeRate(models.Model):
    date = models.DateField()
    this = models.ForeignKey(Currency)
    other = models.ForeignKey(Currency)
    index = models.FloatField()

    def calc(self, value):
        return value * self.index
