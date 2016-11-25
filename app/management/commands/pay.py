from django.core.management.base import BaseCommand
from app.models import Bill, Contract, Message, Action


class Command(BaseCommand):

    def handle(self, *args, **options):
        contracts = Contract.objects.all()
        active_contracts = [contract for contract in contracts if contract.is_active()]
        for contract in active_contracts:
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
