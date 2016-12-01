# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app.management.commands import pay, rates
from app.models import DateDelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        days = DateDelta.objects.get_or_create(name='days')[0]
        days.value += 1
        days.save()
        rates.Command().handle()
        pay.Command().handle()
