from django.core.management.base import BaseCommand, CommandError
from app.models import ExchangeRate
from random import random


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            last_date = ExchangeRate.objects.last().date
        except:
            raise CommandError('No old rates')
        old_exchange_rates = ExchangeRate.objects.all().filter(date=last_date)
        for old_exchange_rate in old_exchange_rates:
            eps = 0.05
            delta = (random() * eps) + 1 - (eps / 2)
            exchange_rate = ExchangeRate(from_currency=old_exchange_rate.from_currency,
                                         to_currency=old_exchange_rate.to_currency,
                                         index=old_exchange_rate.index * delta)
            exchange_rate.save()