from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime


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
    title = models.CharField(max_length=3, verbose_name='Название')
    icon = models.CharField(max_length=1, verbose_name='Значок')

    def __str__(self):
        return self.title


class Bill(models.Model):
    client = models.ForeignKey(User, verbose_name='Клиент')
    money = models.FloatField(verbose_name='Денежная сумма')
    currency = models.ForeignKey(Currency, verbose_name='Валюта')

class Deposit(models.Model):

    Types = (
        ('Вклад до востребования', 'Вклад до востребования'),
        ('Сберегательный вклад', 'Сберегательный вклад'),
        ('Накопительный вклад','Накопительный вклад'),
        ('Расчетный вклад','Расчетный вклад'),
        ('Индексируемый вклад','Индексируемый вклад')
    )

    depositType = models.CharField(max_length=30,choices=Types, verbose_name='Тип')
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=300, verbose_name='Описание')
    currency = models.ForeignKey(Currency, verbose_name='Валюта')
    min_amount = models.PositiveIntegerField(verbose_name='Минимальная сумма')
    duration = models.PositiveIntegerField(verbose_name='Срок хранения (в месяцах)')
    pay_period_in_days = models.PositiveIntegerField(verbose_name='Период выплат (в днях)',default=0)
    percent = models.FloatField(verbose_name='Ставка')
    is_refill=models.BooleanField(verbose_name='Возможность пополнения',default=True)
    min_refill = models.PositiveIntegerField(verbose_name='Минимальное пополнение',blank=True, null=True, default=0)
    is_early_withdrawal=models.BooleanField(verbose_name='Возможность преждевременного снятия',default=False)
    minimum_balance=models.PositiveIntegerField(verbose_name='Неснижаемый остаток', blank=True, null=True, default=0)
    percent_for_early_withdrawal=models.FloatField(verbose_name='ставка при нарушении минимального баланса',blank=True,default=0, null=True)
    is_capitalization=models.BooleanField(verbose_name='Капитализация')
    binding_currency=models.ForeignKey(Currency,related_name="BindingCurrency", verbose_name='Валюта привязки',blank=True,null=True, default=None)
    is_archive=models.BooleanField(verbose_name='В архиве',default=False,editable=False)


    def __str__(self):
        return self.title

    def getCurrencyTitle(self):
        return self.currency.title


class Contract(models.Model):
    bill = models.ForeignKey(Bill, verbose_name='Счёт пользователя',default=None,editable=False,null=True)
    deposit_bill=models.FloatField(verbose_name='Сумма')
    deposit = models.ForeignKey(Deposit, verbose_name='Вид дипозита', editable=False,blank=True, null=True)
    #percent = models.FloatField(verbose_name='Ставка')
    bonuce=models.FloatField(verbose_name='Бонусная индексированная ставка', default=0, editable=False)
    sign_date = models.DateTimeField(verbose_name='Дата подписания', default=datetime.datetime.now, editable=False)
    end_date = models.DateTimeField(verbose_name='Дата окончания',editable=False, default=None,null=True)
    is_prolongation=models.BooleanField(verbose_name='Пролонгация',default=False)

    def get_storing_term(self):
        return (datetime.datetime.now() - self.sign_date).days

    def calculate_bonuce(self):
        self.bonuce=((self.final_exchange_rate/self.start_exchange_rate)*100-100)*360/360


class ActionType(models.Model):
    description=models.CharField(max_length=300, verbose_name='Описание')


class Action(models.Model):
    actionType=models.ForeignKey(ActionType, verbose_name='Тип действия')
    contract = models.ForeignKey(Contract, verbose_name='Договор')
    datetime = models.DateTimeField(verbose_name='Дата', default=datetime.datetime.now)
    money = models.FloatField(verbose_name='Денежная сумма')




class ExchangeRate(models.Model):
    date = models.DateField(verbose_name='Дата', default=datetime.date.today)
    from_currency = models.ForeignKey(Currency, verbose_name='Эталон', related_name="from_currency")
    to_currency = models.ForeignKey(Currency, verbose_name='Валюта', related_name="to_currency")
    index = models.FloatField(verbose_name='Кросс-курс')

    def calc(self, value):
        return value * self.index
