# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Setting(models.Model):
    name = models.CharField(max_length=10)
    value = models.IntegerField(default=0)

    @classmethod
    def get_relativedelta(cls):
        return relativedelta(
            years=Setting.objects.get_or_create(name='years')[0].value,
            months=Setting.objects.get_or_create(name='months')[0].value,
            days=Setting.objects.get_or_create(name='days')[0].value,
            hours=Setting.objects.get_or_create(name='hours')[0].value
        )

    @classmethod
    def set_processing(cls, value):
        param = Setting.objects.get_or_create(name='processing')[0]
        param.value = value
        param.save()


def today():
    return timezone.now().date() + Setting.get_relativedelta()


def now():
    return timezone.now() + Setting.get_relativedelta()


class User(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    father_name = models.CharField(max_length=30, verbose_name='Отчество')
    passport_date = models.DateField(verbose_name='Дата выдачи')
    passport_ser = models.CharField(max_length=9, verbose_name='Серия')
    passport_id = models.CharField(max_length=14, verbose_name='Идентификационный номер')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    birthday = models.DateField(verbose_name='Дата рождения')

    def get_full_name(self):
        return self.username if self.is_superuser else u"{} {} {}".format(self.last_name, self.first_name,
                                                                          self.father_name)

    def get_short_name(self):
        return self.username if self.is_superuser else u"{} {}. {}.".format(self.last_name, self.first_name[:1],
                                                                            self.father_name[:1])

    def get_age(self):
        return (today() - self.birthday).days // 365

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
            return False

    def alert(self, text):
        Alert.objects.create(
            user=self,
            text=text
        )

    def get_alerts(self):
        alerts = Alert.objects.filter(
            user=self
        )
        texts = map(
            lambda alert: alert.text,
            alerts
        )
        alerts.delete()
        return texts


class Currency(models.Model):
    title = models.CharField(max_length=3, verbose_name='Название')
    icon = models.CharField(max_length=1, verbose_name='Значок')

    def __str__(self):
        return self.title

    def format_value(self, value):
        return "{} {}".format(round(value, 2), self.title)

    def from_exchange_rates(self):
        return ExchangeRate.objects.exclude(
            to_currency=self
        ).filter(
            from_currency=self,
            date=today(),
        )

    def to_exchange_rates(self):
        return ExchangeRate.objects.exclude(
            from_currency=self
        ).filter(
            to_currency=self,
            date=today()
        )

    def calc(self, other, value):
        try:
            if self == other:
                return value
            else:
                return ExchangeRate.objects.get(
                    from_currency=self,
                    to_currency=other,
                    date=today()
                ).calc(value)
        except:
            return None


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
            value = self.currency.calc(other.currency, value)
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
    date = models.DateField(default=today, verbose_name='Дата')

    def read(self):
        self.readed = True
        self.save()


class DepositType(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=300, verbose_name='Описание')

    def __str__(self):
        return self.title


class Deposit(models.Model):

    depositType = models.ForeignKey(DepositType, verbose_name='Тип депозита',editable=False)
    title = models.CharField(max_length=50, verbose_name='Название')
    currency = models.ForeignKey(Currency, verbose_name='Валюта')
    min_amount = models.IntegerField(verbose_name='Минимальная сумма')
    is_month = models.BooleanField(verbose_name='Счет времени в месяцах', default=True)
    duration = models.IntegerField(verbose_name='Срок хранения', default=0)
    pay_period = models.IntegerField(verbose_name='Период выплат')
    percent = models.FloatField(verbose_name='Ставка')

    is_refill = models.BooleanField(verbose_name='Возможность пополнения', default=False, editable=False)
    min_refill = models.IntegerField(verbose_name='Минимальное пополнение', default=0)
    is_early_withdrawal = models.BooleanField(verbose_name='Возможность частичного снятия', default=False,
                                              editable=False)
    minimum_balance = models.IntegerField(verbose_name='Неснижаемый остаток', default=0)
    percent_for_early_withdrawal = models.FloatField(verbose_name='ставка при нарушении неснижаемого остатка', default=0)
    is_capitalization = models.BooleanField(verbose_name='Капитализация')
    binding_currency = models.ForeignKey(Currency, related_name="BindingCurrency", verbose_name='Валюта привязки', default=None, null=True)
    is_archive = models.BooleanField(verbose_name='В архиве', default=False, editable=False)

    def __str__(self):
        return self.title

    def format_duration(self):
        if self.duration==0:
            return "нет ограничений"
        interval = "месяцев" if self.is_month else "дней"
        return "{} {}".format(self.duration, interval)

    def format_pay_period(self):
        interval = "месяцев" if self.is_month else "дней"
        return "{} {}".format(self.pay_period, interval)

    def format_min_amount(self):
        return self.currency.format_value(self.min_amount)

    def format_refill(self):
        if self.is_refill:
            if self.min_refill==0:
                return 'Да'
            return 'Мин. '+self.currency.format_value(self.min_refill)
        else:
            return 'Нет'

    def format_withdrawal(self):
        if self.is_early_withdrawal:
            if self.minimum_balance==0:
                return 'Да'
            return  'Неснижаемый остаток: '+self.currency.format_value(self.minimum_balance)
        else:
            return 'Нет'

    def format_capitalization(self):
        if self.is_capitalization:
            return "Да"
        return "Нет"


class Contract(models.Model):
    deposit = models.ForeignKey(Deposit, verbose_name='Вид дипозита', editable=False)
    start_amount = models.IntegerField(verbose_name='Сумма')
    bill = models.ForeignKey(Bill, verbose_name='Счет привязки')
    deposit_bill = models.ForeignKey(Bill, verbose_name='Депозитный счет', related_name='deposit_bill', editable=False)
    sign_date = models.DateField(verbose_name='Дата подписания', default=today, editable=False)
    end_date = models.DateField(verbose_name='Дата окончания', editable=False, null=True)
    is_use_percent_for_early_withdrawal=models.BooleanField(verbose_name='изменить процентную ставку', default=False,editable=False)
    is_act=models.BooleanField(verbose_name='Активен', default=True, editable=False)

    def refill(self, amount, bill):
        min_refill = self.deposit.currency.calc(bill.currency, self.deposit.min_refill)
        _sub_bill_amount = amount
        amount = bill.currency.calc(self.deposit.currency, amount)

        if self.deposit.is_refill and amount >= self.deposit.min_refill:
            if bill.pop(_sub_bill_amount):
                self.deposit_bill.push(amount)
                return [True]
            else:
                return [False, 'Недостаточно средств ({0} {1})'.format(bill.money, bill.currency.title)]
        else:
            return [False, 'Минимальное пополнение: ' + str(min_refill) + str(bill.currency.title)]

    def withdraw(self, amount, necessarily=False):
        if self.deposit.is_early_withdrawal and self.deposit_bill.money-amount>=self.deposit.minimum_balance:
            self.bill.push(amount)
            self.deposit_bill.pop(amount)
            return True
        elif necessarily and self.deposit_bill.money - amount >= 0:
            self.bill.push(amount)
            self.deposit_bill.pop(amount)
            self.is_use_percent_for_early_withdrawal=True
            return True
        return False

    def calculate_payment(self):
        last_pay_date = self.get_last_pay_date()

        return self.deposit_bill.money * (self.get_percent() / 100) * (today() - last_pay_date).days / 365

    def get_percent(self):
        if self.is_use_percent_for_early_withdrawal:
            return self.deposit.percent_for_early_withdrawal
        return self.deposit.percent

    def pay(self, value, action='PAY', to_itself=False):
        target_bill = self.deposit_bill if to_itself else self.bill
        target_bill.push(value, action)

    def super_pay(self):
        if self.sign_date < today() and self.is_active():
            sum = self.calculate_payment()
            if self.is_needs_pay() and sum > 0:
                print(sum, today())
                self.pay(sum, to_itself=self.deposit.is_capitalization)
            if (self.end_date and (today() - self.end_date).days >= 0) or self.deposit_bill.money == 0:
                print("Close")
                self.close()

    def close(self):
        self.is_act = False
        if self.end_date == None:
            self.end_date = today()
        self.save()
        if self.deposit.binding_currency and today() >= self.end_date and self.calculate_bonuce() > 0:
            self.pay(self.calculate_bonuce(), to_itself=False, action='PAY BONUCE')
        self.pay(self.deposit_bill.money, to_itself=False, action='CLOSE DEPOSIT')
        self.deposit_bill.pop(self.deposit_bill.money)
        return

    def calculate_end_date(self):
        if self.deposit.duration == 0:
            self.end_date = None
        elif self.deposit.is_month:
            self.end_date = self.sign_date + relativedelta(months=self.deposit.duration)
        else:
            self.end_date = self.sign_date + relativedelta(days=self.deposit.duration)
        self.save()

    def is_active(self):
        return self.is_act

    def get_duration_in_days(self):
        return (self.end_date - self.sign_date).days

    def get_storing_term(self):
        return (today() - self.sign_date).days

    def calculate_bonuce(self):
        exchange_rates = ExchangeRate.objects.filter(
            from_currency=self.deposit.currency,
            to_currency=self.deposit.binding_currency
        )
        sign_rate = exchange_rates.get(date=self.sign_date)
        today_rate = exchange_rates.get(date=today())

        return self.deposit_bill.money * (
        (today_rate.index / sign_rate.index) * 100 - 100) * self.get_storing_term() / 365

    def prolongation_to_string(self):
        if self.is_prolongation:
            return "Yes"
        return "No"

    def is_needs_pay(self):
        last_pay_date = self.get_last_pay_date()
        if self.deposit.is_month:
            timedelta = relativedelta(today(), last_pay_date).months
        else:
            timedelta = relativedelta(today(), last_pay_date).days

        if timedelta >= self.deposit.pay_period:
            return True
        else:
            return False

    def get_actions(self):
        return Action.objects.filter(
            bill=self.deposit_bill
        )

    def get_last_pay_date(self):
        try:
            return self.get_actions().filter(
                actionType=ActionType.objects.get(description='PAY')
            ).last().datetime.date()
        except:
            return self.sign_date

    def get_relative_pay_period(self):
        if self.deposit.is_month:
            return relativedelta(months=self.deposit.pay_period)
        else:
            return relativedelta(days=self.deposit.pay_period)


class ActionType(models.Model):
    description = models.CharField(max_length=300, verbose_name='Описание')

    def __str__(self):
        return self.description


class Action(models.Model):
    actionType = models.ForeignKey(ActionType, verbose_name='Тип действия')
    bill = models.ForeignKey(Bill, verbose_name='Счёт пользователя', default=None, editable=False, null=True)
    datetime = models.DateTimeField(verbose_name='Дата', default=now)
    money = models.FloatField(verbose_name='Денежная сумма')

    @classmethod
    def add(cls, action=None, bill=None, money=0, datetime=now()):
        Action.objects.create(
            actionType=ActionType.objects.get_or_create(description=action)[0],
            bill=bill,
            money=money,
            datetime=datetime
        ).save()

    def format_money(self):
        try:
            return self.bill.currency.format_value(self.money)
        except:
            return None

    def __str__(self):
        return self.actionType


class ExchangeRate(models.Model):
    date = models.DateField(verbose_name='Дата', default=today)
    from_currency = models.ForeignKey(Currency, verbose_name='Эталон', related_name="from_currency")
    to_currency = models.ForeignKey(Currency, verbose_name='Валюта', related_name="to_currency")
    index = models.FloatField(verbose_name='Кросс-курс')

    def calc(self, value):
        return value * self.index


class Alert(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=300)
