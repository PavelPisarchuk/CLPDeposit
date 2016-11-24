from django.core.management.base import BaseCommand
from app.models import Contract, Message, Pay


class Command(BaseCommand):

    def handle(self, *args, **options):
        contracts = Contract.objects.all()
        active_contracts = [contract for contract in contracts if contract.is_active()]
        for contract in active_contracts:
            pay = Pay.objects.create(
                contract=contract,
                money=contract.calc_payment()
            )
            Message.objects.create(
                message="Вам выплачено {} по вкладу {}".format(
                    contract.deposit.currency.print_full(pay.money),
                    contract.deposit.title
                ),
                header='Выплата по вкладу',
                user=contract.bill.client
            )