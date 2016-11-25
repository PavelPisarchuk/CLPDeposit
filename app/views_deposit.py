from django.shortcuts import render, redirect
from app.models import Deposit


def list(request, deposit_id=None):
    if deposit_id != None:
        d = Deposit.objects.get(pk=deposit_id)
        d.is_archive = True
        d.save()
    depositList = Deposit.objects.all()
    return render(request, 'deposit/list_admin.html', {'depositList': depositList})


def open(request):
    return


def refill(request):
    return


def transfer(request):
    return


def close(request):
    return


def extract(request):
    return


def history(request):
    return