# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app.models import Contract, Setting


class Command(BaseCommand):

    def handle(self, *args, **options):
        Setting.set_processing(True)
        pay_contracts = [contract for contract in Contract.objects.all() if
                         contract.is_active() and contract.is_needs_pay()]
        for contract in pay_contracts:
            payment = contract.calculate_payment()
            contract.pay(
                payment,
                datetime=contract.get_last_pay_date()
            )
            contract.bill.client.send_message(
                header='Выплата по вкладу',
                message="Вам выплачено {} по вкладу {}".format(
                    payment,
                    contract.deposit.title
                )
            )
        Setting.set_processing(False)
