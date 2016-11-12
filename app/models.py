from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    father_name = models.CharField(max_length=30, verbose_name='Отчество')
    passport_id = models.CharField(max_length=14, verbose_name='Идентификационный номер')
    phone = models.CharField(max_length=13, verbose_name='Телефон')
    address = models.CharField(max_length=50, verbose_name='Адрес')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    def get_full_name(self):
        return self.username if self.is_superuser else "{} {} {}".format(self.last_name, self.first_name, self.father_name)

    def get_short_name(self):
        return self.username if self.is_superuser else "{} {}. {}.".format(self.last_name, self.first_name[:1], self.father_name[:1])

    def get_age(self):
        from datetime import date
        return (date.today() - self.birthday).days // 365


class Currency(models.Model):
    title = models.CharField(max_length=2, verbose_name='Название')
    icon = models.CharField(max_length=1, verbose_name='Значок')


class Bill(models.Model):
    client = models.ForeignKey(User, verbose_name='Клиент')
    money = models.FloatField(verbose_name='Денежная сумма')
    currency = models.ForeignKey(Currency, verbose_name='Валюта')


class Deposit(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание')
    percent = models.IntegerField(verbose_name='Ставка')
    min_storing_term = models.IntegerField(verbose_name='Минимальный срок хранения')
    max_storing_term = models.IntegerField(verbose_name='Максимальный срок хранения')
    pay_term = models.IntegerField(verbose_name='Период выплат')
    refill = models.BooleanField(verbose_name='Пополнение')
    partial_take = models.BooleanField(verbose_name='Частичное снятие')
    indexed = models.BooleanField(verbose_name='Индексированный')
    currency = models.ForeignKey(Currency, verbose_name='Валюта')


class Contract(models.Model):
    bill = models.ForeignKey(Bill, verbose_name='Счёт')
    deposit = models.ForeignKey(Deposit, verbose_name='Вклад')
    sign_date = models.DateTimeField(verbose_name='Дата подписания')
    term = models.IntegerField(verbose_name='Срок')
    money = models.FloatField(verbose_name='Сумма вклада')

    def get_storing_term(self):
        from datetime import date
        return (date.today() - self.sign_date).days


class Pay(models.Model):
    agent = models.ForeignKey(User, verbose_name='Оформитель')
    contract = models.ForeignKey(Contract, verbose_name='Договор')
    datetime = models.DateTimeField(verbose_name='Дата')
    money = models.FloatField(verbose_name='Денежная сумма')


class ExchangeRate(models.Model):
    date = models.DateField(verbose_name='Дата')
    from_currency = models.ForeignKey(Currency, verbose_name='Эталон', related_name="from_currency")
    to_currency = models.ForeignKey(Currency, verbose_name='Валюта', related_name="to_currency")
    index = models.FloatField(verbose_name='Кросс-курс')

    def calc(self, value):
        return value * self.index
