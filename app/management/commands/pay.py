# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import datetime

from app.models import Bill, Contract, Message, Action


class Command(BaseCommand):

    def handle(self, *args, **options):
        contracts = Contract.objects.all()
        active_contracts = [contract for contract in contracts if contract.is_active()]
        for contract in active_contracts:
            last_pay = Action.get_last_pay(contract)
            if last_pay:
                print('no')
                last_pay_date = last_pay.datetime
                if contract.deposit.is_pay_period_month:
                    d1, d2 = datetime.datetime.now(), last_pay_date
                    timedelta = (d1.year - d2.year) * 12 + d1.month - d2.month
                else:
                    timedelta = (datetime.date.today() - last_pay_date.date()).days

            if not last_pay or timedelta >= contract.deposit.pay_period:
                pay = 500
                Action.add(
                    action_type_title='PAY',
                    contract=contract,
                    money=pay
                )
                contract.bill.push(pay)

                Message.objects.create(
                    message="Вам выплачено {} по вкладу {}".format(
                        pay,
                        contract.deposit.title
                    ),
                    header='Выплата по вкладу',
                    user=contract.bill.client
                ).save()
