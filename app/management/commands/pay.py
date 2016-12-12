# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app.models import Contract, Setting


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Setting.set_processing(True)
            pay_contracts = Contract.objects.filter(
                is_act=True
            )
            for contract in pay_contracts:
                contract.super_pay()
        finally:
            Setting.set_processing(False)
