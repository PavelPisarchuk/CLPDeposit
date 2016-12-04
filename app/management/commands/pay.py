# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app.models import Contract, Setting


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Setting.set_processing(True)
            pay_contracts = Contract.objects.all()
            for contract in pay_contracts:
                pass
        finally:
            Setting.set_processing(False)
