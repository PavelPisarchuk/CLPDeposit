# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app.models import Setting


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Setting.set_processing(True)
            hours = Setting.objects.get_or_create(name='hours')[0]
            hours.value += 1
            hours.save()
        finally:
            Setting.set_processing(False)
