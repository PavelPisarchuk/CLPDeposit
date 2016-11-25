from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from app.forms import *


@user_passes_test(lambda u: u.is_superuser)
def list(request, deposit_id=None):
    if deposit_id != None:
        d = Deposit.objects.get(pk=deposit_id)
        d.is_archive = True
        d.save()
    depositList = Deposit.objects.all()
    return render(request, 'deposit/list.html', {'depositList': depositList})


@user_passes_test(lambda u: u.is_superuser)
def new(request):
    errors=[]
    if request.method == 'POST':
        depositForm = DepositForm(request.POST)
        if depositForm.is_valid():
            d=depositForm.save(commit=False)
            if d.percent<=0:
                errors.append('Percent must be bigger then 0')
            elif d.depositType!='Вклад до востребования' and (d.percent_for_early_withdrawal==None or d.percent_for_early_withdrawal<=0):
                errors.append('percent for early withdrawal must be bigger then 0')
            elif d.depositType=='Индексируемый вклад' and d.binding_currency==None:
                errors.append('add binding currency')
            else:
                d.save()
                return redirect('deposit:list')
    else:
        depositForm = DepositForm()

    return render(request, 'deposit/new.html', {'depositForm': depositForm, 'errors':errors})


@user_passes_test(lambda u: u.is_superuser)
def edit(request, deposit_id):
    errors=[]
    oldDeposit = Deposit.objects.get(pk=deposit_id)

    if request.method == 'POST':
        depositForm = DepositForm(request.POST)
        if depositForm.is_valid():
            d=depositForm.save(commit=False)
            if d.percent<=0:
                errors.append('Percent must be bigger then 0')
            elif d.depositType!='Вклад до востребования' and (d.percent_for_early_withdrawal==None or d.percent_for_early_withdrawal<=0):
                errors.append('percent for early withdrawal must be bigger then 0')
            elif d.depositType=='Индексируемый вклад' and d.binding_currency==None:
                errors.append('add binding currency')
            else:
                oldDeposit.is_archive=True;
                oldDeposit.save()
                d.save()
                return redirect('deposit:list')
    else:
        depositForm = DepositForm(instance=oldDeposit)

    return render(request, 'deposit/edit.html', {'depositForm': depositForm, 'errors':errors, 'ID':deposit_id})


@user_passes_test(lambda u: u.is_superuser)
def currency(request):
    currencyList=Currency.objects.all()

    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            form = CurrencyForm()
    else:
        form = CurrencyForm()

    return render(request, 'deposit/currency.html', {'form': form, 'currencyList':currencyList})


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