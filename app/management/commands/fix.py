# -*- coding: utf-8 -*-
from random import random

from django.core.management.base import BaseCommand

from app.models import Contract, Bill, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            user.set_password(user.username)
            user.save()
        for contract in Contract.objects.all():
            contract.calculate_end_date()
            contract.start_amount = contract.deposit.min_amount + random() * 100
            contract.save()
            bill1 = Bill.objects.get(id=contract.bill_id)
            bill2 = Bill.objects.get(id=contract.deposit_bill_id)
            bill1.currency = contract.deposit.currency
            bill2.currency = contract.deposit.currency
            bill2.money = contract.start_amount
            bill1.save()
            bill2.save()
