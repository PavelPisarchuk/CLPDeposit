# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app.models import Contract


class Command(BaseCommand):

    def handle(self, *args, **options):
        pay_contracts = [contract for contract in Contract.objects.all() if contract.is_active() and contract.is_needs_pay()]
        for contract in pay_contracts:
            pay = 500
            contract.bill.push(pay, 'PAY')
            contract.bill.client.send_message(
                header='Выплата по вкладу',
                message="Вам выплачено {} по вкладу {}".format(
                    pay,
                    contract.deposit.title
                )
            )
