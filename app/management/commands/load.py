# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.core.management.base import BaseCommand

from app.management.commands import rates
from app.models import Setting


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Setting.set_processing(True)
            call_command('loaddata', 'users', app_label='app')
            call_command('loaddata', 'currencies', app_label='app')
            call_command('loaddata', 'exchangerate', app_label='app')
            call_command('loaddata', 'bill', app_label='app')
            call_command('loaddata', 'DepositType', app_label='app')
            call_command('loaddata', 'Deposit', app_label='app')
            rates.Command().handle()
        finally:
            Setting.set_processing(False)
