# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app.models import DateDelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        hours = DateDelta.objects.get_or_create(name='hours')[0]
        hours.value += 1
        hours.save()
