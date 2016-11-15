from app.models import ExchangeRate
from random import random


def fill_exchange_rates():
    last_date = ExchangeRate.objects.last().date
    old_exchange_rates = ExchangeRate.objects.all().filter(date=last_date)
    for old_exchange_rate in old_exchange_rates:
        eps = 0.05
        delta = (random() * eps) + 1 - (eps / 2)
        exchange_rate = ExchangeRate(from_currency=old_exchange_rate.from_currency,
                                     to_currency=old_exchange_rate.to_currency,
                                     index=old_exchange_rate.index * delta)
        exchange_rate.save()
