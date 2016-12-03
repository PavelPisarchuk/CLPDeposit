# -*- coding: utf-8 -*-
from random import random

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError

from app.models import ExchangeRate, Setting
from app.models import today as t


class Command(BaseCommand):

    def handle(self, *args, **options):
        Setting.set_processing(True)
        eps = 0.05
        try:
            rates = ExchangeRate.objects.all()
            last_date = rates.last().date
            last_rates = rates.filter(date=last_date)
        except:
            raise CommandError('No old rates')
        today = t()
        while last_date != today:
            next_date = last_date + relativedelta(days=1)
            next_rates = []
            for rate in last_rates:
                delta = (random() * eps) + 1 - (eps / 2)
                exchange_rate = ExchangeRate(
                    date=next_date,
                    from_currency=rate.from_currency,
                    to_currency=rate.to_currency,
                    index=rate.index * delta
                )
                next_rates.append(exchange_rate)
                exchange_rate.save()
            last_date, last_rates = next_date, next_rates
        Setting.set_processing(False)
