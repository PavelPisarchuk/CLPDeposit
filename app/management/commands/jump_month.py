# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand

from app.management.commands import jump_day
from app.models import Setting, today


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            days = ((today() + relativedelta(months=1)) - today()).days
            jump = jump_day.Command()
            for _ in range(days):
                jump.handle()
        finally:
            Setting.set_processing(False)
