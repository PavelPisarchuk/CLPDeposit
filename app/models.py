# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models


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

    def get_messages(self):
        return Message.objects.filter(
            user=self
        )

    def get_unread_messages_count(self):
        return self.get_messages().filter(readed=False).count()

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
            bill=obj,
            money=money
        )
        return obj

    def get_bills(self):
        return Bill.objects.filter(
            client=self,
            is_private=True
        )

    def get_contracts(self):
        return Contract.objects.filter(
            bill__client=self
        )

    def change_password(self, old, new, repeat):
        if self.check_password(old) and new == repeat:
            self.set_password(new)
            self.save()
            return True
        else:
            raise

class Currency(models.Model):
    title = models.CharField(max_length=3, verbose_name='Название')
    icon = models.CharField(max_length=1, verbose_name='Значок')

    def __str__(self):
        return self.title

    def format_value(self, value):
        return "{}{}".format(self.title, round(value, 2))

    def from_exchange_rates(self):
        return ExchangeRate.objects.exclude(
            to_currency=self
        ).filter(
            from_currency=self,
            date=datetime.date.today(),
        )

    def to_exchange_rates(self):
        return ExchangeRate.objects.exclude(
            from_currency=self
        ).filter(
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

    def push(self, value, action='FILL'):
        self.money += value
        self.save()
        Action.add(
            action=action,
            bill=self,
            money=value
        )

    def pop(self, value, action='TAKE_PART'):
        if self.money >= value:
            self.money -= value
            self.save()
            Action.add(
                action=action,
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

    def __str__(self):
        return "Счет #{}".format(self.id)

    def get_cards(self):
        return Card.objects.filter(
            bill=self
        )

    def get_actions(self):
        return Action.objects.filter(
            bill=self
        )

    def transfer(self, other, value):
        if self.pop(value):
            other.push(value)
            return True
        else:
            return False


class Card(models.Model):
    bill = models.ForeignKey(Bill, verbose_name='Счёт')
    limit = models.FloatField(verbose_name='Лимит')


class Message(models.Model):
    message = models.CharField(max_length=300, verbose_name='Сообщение')
    header = models.CharField(max_length=100, verbose_name='Заголовок')
    readed = models.BooleanField(default=False, verbose_name='Прочитано?')
    user = models.ForeignKey(User, verbose_name='Пользователь')
    date = models.DateField(default=datetime.date.today, verbose_name='Дата')

    def read(self):
        self.readed = True
        self.save()


class DepositType(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=300, verbose_name='Описание')

    def __str__(self):
        return self.title

class Deposit(models.Model):

    Types = (
        ('Вклад до востребования', 'Вклад до востребования'),
        ('Сберегательный вклад', 'Сберегательный вклад'),
        ('Накопительный вклад', 'Накопительный вклад'),
        ('Расчетный вклад', 'Расчетный вклад'),
        ('Индексируемый вклад', 'Индексируемый вклад')
    )

    depositType = models.ForeignKey(DepositType, verbose_name='Тип депозита')
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=300, verbose_name='Описание')
    currency = models.ForeignKey(Currency, verbose_name='Валюта')
    min_amount = models.PositiveIntegerField(verbose_name='Минимальная сумма')
    duration = models.PositiveIntegerField(verbose_name='Срок хранения (в месяцах)', default=0)
    is_pay_period_month = models.BooleanField(verbose_name='Период выплат в месяцах', default=False)
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

    def format_duration(self):
        if self.duration==0:
            return "нет ограничений"
        return "{} месяцев".format(self.duration)

    def format_pay_period(self):
        interval = "месяцев" if self.is_pay_period_month else "дней"
        return "{} {}".format(self.pay_period, interval)

    def format_min_amount(self):
        return self.currency.format_value(self.min_amount)


class Contract(models.Model):
    deposit = models.ForeignKey(Deposit, verbose_name='Вид дипозита', editable=False, blank=True, null=True)
    start_amount=models.PositiveIntegerField(verbose_name='Сумма')
    bill = models.ForeignKey(Bill, verbose_name='Счет привязки')
    deposit_bill = models.ForeignKey(Bill,verbose_name='Депозитный счет',related_name='deposit_bill',editable=False, blank=True, null=True)
    bonus = models.FloatField(verbose_name='Бонусная индексированная ставка', default=0, editable=False)
    sign_date = models.DateTimeField(verbose_name='Дата подписания', default=datetime.datetime.now, editable=False)
    end_date = models.DateTimeField(verbose_name='Дата окончания', editable=False, default=None, null=True)
    is_use_percent_for_early_withdrawal=models.BooleanField(verbose_name='изменить процентную ставку', default=False,editable=False)
    is_prolongation = models.BooleanField(verbose_name='Пролонгация', default=False)
    is_acttt=models.BooleanField(verbose_name='Активен', default=True)

    def push(self, value, action='FILL'):
        self.deposit_bill += value
        self.save()
        Action.add(
            action=action,
            bill=self,
            money=value
        )

    def pop(self, value, action='TAKE_PART'):
        if self.money >= value:
            self.money -= value
            self.save()
            Action.add(
                action=action,
                bill=self,
                money=value
            )
            return True
        else:
            return False

    def refill(self,amount):
        if self.deposit.is_refill and self.bill.currency==self.deposit.currency and amount>=self.deposit.min_refill:
            if self.bill.pop(amount):
                self.deposit_bill+=amount
                return True
            else:
                return False
        else:
            return False


    def withdraw(self, amount, necessarily=False):
        if self.deposit.is_early_withdrawal and self.deposit_bill-amount>=self.deposit.minimum_balance:
            self.bill.push(amount)
            self.deposit_bill-=amount
            return True
        elif necessarily and self.deposit_bill-amount>=0:
            self.bill.push(amount)
            self.deposit_bill-=amount
            self.is_use_percent_for_early_withdrawal=True
            return True
        return False

    def close(self):
        return


    def calculate_payment(self):
        return self.deposit_bill*self.deposit.percent*(datetime.datetime.now-self.get_last_pay().datetime).days/365


    def calculate_end_date(self):
        if self.deposit.duration==0:
            self.end_date=None
            return

        if self.deposit.is_pay_period_month:
            self.end_date = self.sign_date + relativedelta(months=self.deposit.duration)
        else:
            self.end_date = self.sign_date + datetime.timedelta(days=self.deposit.duration)

    def is_active(self):
        if self.end_date is None:
            return True
        else:
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
        self.bonus = ((today_rate / sign_rate) * 100 - 100) * 365 / self.get_storing_term()

    def prolongation_to_string(self):
        if self.is_prolongation:
            return "Yes"
        return "No"

    def is_needs_pay(self):
        last_pay = self.get_last_pay()
        if not last_pay:
            last_pay_date = self.sign_date
        else:
            last_pay_date = last_pay.datetime

        if self.deposit.is_pay_period_month:
            timedelta = relativedelta(datetime.datetime.now(), last_pay_date).months
        else:
            timedelta = (datetime.datetime.now() - last_pay_date).days

        if timedelta >= self.deposit.pay_period:
            return True
        else:
            return False

    def get_actions(self):
        return Action.objects.filter(
            contract=self
        )

    def get_last_pay(self):
        return self.get_actions().filter(
            actionType=ActionType.objects.get(description='PAY')
        ).last()

    def push(self, value, action='FILL'):
        self.deposit_bill += value
        self.save()
        Action.add(
            action=action,
            contract=self,
            money=value
        )

    def pay(self, value, action='PAY'):
        Action.add(
            action=action,
            contract=self,
            money=value
        )
        if self.deposit.is_capitalization:
            self.push(value, action)
        else:
            self.bill.push(value, action)


class ActionType(models.Model):
    description = models.CharField(max_length=300, verbose_name='Описание')

    def __str__(self):
        return self.description


class Action(models.Model):
    actionType = models.ForeignKey(ActionType, verbose_name='Тип действия')
    contract = models.ForeignKey(Contract, verbose_name='Договор', default=None, editable=False, null=True)
    bill = models.ForeignKey(Bill, verbose_name='Счёт пользователя', default=None, editable=False, null=True)
    datetime = models.DateTimeField(verbose_name='Дата', default=datetime.datetime.now)
    money = models.FloatField(verbose_name='Денежная сумма')

    @classmethod
    def add(cls, action=None, contract=None, bill=None, money=0):
        Action.objects.create(
            actionType=ActionType.objects.get_or_create(description=action)[0],
            contract=contract,
            bill=bill,
            money=money
        ).save()

    def format_money(self):
        if self.bill:
            return self.bill.currency.format_value(self.money)
        elif self.contract:
            return self.contract.deposit.currency.format_value(self.money)

    def __str__(self):
        return self.actionType


class ExchangeRate(models.Model):
    date = models.DateField(verbose_name='Дата', default=datetime.date.today)
    from_currency = models.ForeignKey(Currency, verbose_name='Эталон', related_name="from_currency")
    to_currency = models.ForeignKey(Currency, verbose_name='Валюта', related_name="to_currency")
    index = models.FloatField(verbose_name='Кросс-курс')

    def calc(self, value):
        return value * self.index
