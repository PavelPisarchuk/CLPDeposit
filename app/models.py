# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime


class User(AbstractUser):
    #first_name = models.CharField(max_length=30, verbose_name='Имя')
    #last_name = models.CharField(max_length=30, verbose_name='Фамилия')
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
        return (datetime.date.today() - self.birthday).days // 365

    def send_message(self, header, message):
        Message.objects.create(
            user=self,
            header=header,
            message=message
        ).save()

    def add_bill(self, currency, money, is_private):
        obj = Bill.objects.create(
            client=self,
            money=money,
            currency=currency,
            is_private=is_private
        )
        obj.save()
        Action.add(
            action='CREATE',
            bill=self,
            money=money
        )
        return obj


class Currency(models.Model):
    title = models.CharField(max_length=3, verbose_name='Название')
    icon = models.CharField(max_length=1, verbose_name='Значок')

    def __str__(self):
        return self.title

    def format_value(self, value):
        return "{}{}".format(self.title, round(value, 2))

    def from_exchange_rates(self):
        return ExchangeRate.objects.filter(
            from_currency=self,
            date=datetime.date.today()
        )

    def to_exchange_rates(self):
        return ExchangeRate.objects.filter(
            to_currency=self,
            date=datetime.date.today()
        )


class Bill(models.Model):
    client = models.ForeignKey(User, verbose_name='Клиент')
    money = models.FloatField(verbose_name='Денежная сумма', default=0)
    currency = models.ForeignKey(Currency, verbose_name='Валюта')
    is_private = models.BooleanField(verbose_name='Личный счет?', default=True)

    def add_card(self, limit):
        Card.objects.create(
            bill=self,
            limit=limit
        ).save()

    def push(self, value):
        self.money += value
        self.save()
        Action.add(
            action='FILL',
            bill=self,
            money=value
        )

    def pop(self, value):
        if self.money >= value:
            self.money -= value
            self.save()
            Action.add(
                action='TAKE',
                bill=self,
                money=value
            )
            return True
        else:
            return False

    def value_in_currency(self):
        return self.currency.format_value(self.money)

    def toString(self):
        return "Счет #{}".format(self.id)


class Card(models.Model):
    bill = models.ForeignKey(Bill, verbose_name='Счёт')
    limit = models.FloatField(verbose_name='Лимит')


class Message(models.Model):
    message = models.CharField(max_length=300, verbose_name='Сообщение')
    header = models.CharField(max_length=100, verbose_name='Заголовок')
    readed = models.BooleanField(default=False, verbose_name='Прочитано?')
    user = models.ForeignKey(User, verbose_name='Пользователь')
    date = models.DateField(default=datetime.date.today, verbose_name='Дата')


class Deposit(models.Model):

    Types = (
        ('Вклад до востребования', 'Вклад до востребования'),
        ('Сберегательный вклад', 'Сберегательный вклад'),
        ('Накопительный вклад', 'Накопительный вклад'),
        ('Расчетный вклад', 'Расчетный вклад'),
        ('Индексируемый вклад', 'Индексируемый вклад')
    )

    depositType = models.CharField(max_length=30, choices=Types, verbose_name='Тип')
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=300, verbose_name='Описание')
    currency = models.ForeignKey(Currency, verbose_name='Валюта')
    min_amount = models.PositiveIntegerField(verbose_name='Минимальная сумма')
    duration = models.PositiveIntegerField(verbose_name='Срок хранения (в месяцах)')
    is_pay_period_month = models.BooleanField(verbose_name='Период выплат день/месяц', default=False)
    pay_period = models.PositiveIntegerField(verbose_name='Период выплат')
    percent = models.FloatField(verbose_name='Ставка')
    is_refill = models.BooleanField(verbose_name='Возможность пополнения', default=True)
    min_refill = models.PositiveIntegerField(verbose_name='Минимальное пополнение', blank=True, null=True, default=0)
    is_early_withdrawal = models.BooleanField(verbose_name='Возможность преждевременного снятия', default=False)
    minimum_balance = models.PositiveIntegerField(verbose_name='Неснижаемый остаток', blank=True, null=True, default=0)
    percent_for_early_withdrawal = models.FloatField(verbose_name='ставка при нарушении минимального баланса', blank=True, default=0, null=True)
    is_capitalization = models.BooleanField(verbose_name='Капитализация')
    binding_currency = models.ForeignKey(Currency, related_name="BindingCurrency", verbose_name='Валюта привязки', blank=True, null=True, default=None)
    is_archive = models.BooleanField(verbose_name='В архиве', default=False, editable=False)

    def __str__(self):
        return self.title

    def getCurrencyTitle(self):
        return self.currency.title


class Contract(models.Model):
    deposit = models.ForeignKey(Deposit, verbose_name='Вид дипозита', editable=False, blank=True, null=True)
    bill = models.ForeignKey(Bill, verbose_name='Счёт пользователя', default=None, editable=False, null=True)
    deposit_bill = models.FloatField(verbose_name='Сумма')
    bonus = models.FloatField(verbose_name='Бонусная индексированная ставка', default=0, editable=False)
    sign_date = models.DateTimeField(verbose_name='Дата подписания', default=datetime.datetime.now, editable=False)
    end_date = models.DateTimeField(verbose_name='Дата окончания', editable=False, default=None, null=True)
    is_prolongation = models.BooleanField(verbose_name='Пролонгация', default=False)

    def is_active(self):
        tz_info = self.sign_date.tzinfo
        return self.sign_date < datetime.datetime.now(tz_info) < self.end_date

    def get_duration_in_days(self):
        return (self.end_date - self.sign_date).days

    def get_storing_term(self):
        return (datetime.datetime.now() - self.sign_date).days

    def calculate_bonuce(self):
        sign_rate = ExchangeRate.objects.get(
            date=self.sign_date,
            from_currency=self.deposit.currency,
            to_currency=self.deposit.binding_currency
        )
        today_rate = ExchangeRate.objects.get(
            date=datetime.date.today(),
            from_currency=self.deposit.currency,
            to_currency=self.deposit.binding_currency
        )
        self.bonus = ((today_rate / sign_rate) * 100 - 100) * self.get_duration_in_days() / self.get_storing_term()

    def prolongation_to_string(self):
        if self.is_prolongation:
            return "Yes"
        return "No"


class ActionType(models.Model):
    description = models.CharField(max_length=300, verbose_name='Описание')


class Action(models.Model):
    actionType = models.ForeignKey(ActionType, verbose_name='Тип действия')
    contract = models.ForeignKey(Contract, verbose_name='Договор', default=None, editable=False, null=True)
    bill = models.ForeignKey(Bill, verbose_name='Счёт пользователя', default=None, editable=False, null=True)
    datetime = models.DateTimeField(verbose_name='Дата', default=datetime.datetime.now)
    money = models.FloatField(verbose_name='Денежная сумма')

    @classmethod
    def add(cls, action=None, contract=None, bill=None, money=0):
        Action.objects.create(
            actionType=ActionType.objects.get(description=action),
            contract=contract,
            bill=bill,
            money=money
        ).save()

    @classmethod
    def get_last_pay(cls, contract):
        return Action.objects.all().filter(
            actionType=ActionType.objects.get(description='PAY'),
            contract=contract
        ).last()


class ExchangeRate(models.Model):
    date = models.DateField(verbose_name='Дата', default=datetime.date.today)
    from_currency = models.ForeignKey(Currency, verbose_name='Эталон', related_name="from_currency")
    to_currency = models.ForeignKey(Currency, verbose_name='Валюта', related_name="to_currency")
    index = models.FloatField(verbose_name='Кросс-курс')

    def calc(self, value):
        return value * self.index
