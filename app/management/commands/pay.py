# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app.models import Contract


class Command(BaseCommand):

    def handle(self, *args, **options):
        pay_contracts = [contract for contract in Contract.objects.all() if contract.is_active()]
        for contract in pay_contracts:
            payment = contract.calculate_payment()
            contract.pay(payment)
            contract.bill.client.send_message(
                header='Выплата по вкладу',
                message="Вам выплачено {} по вкладу {}".format(
                    payment,
                    contract.deposit.title
                )
            )
