# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.core.management.base import BaseCommand

from app.models import Setting


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Setting.set_processing(True)
            call_command('loaddata', '100/users', app_label='app')
            call_command('loaddata', '100/bill', app_label='app')
            call_command('loaddata', '100/contract', app_label='app')
        finally:
            Setting.set_processing(False)
