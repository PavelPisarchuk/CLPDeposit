# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.forms import modelform_factory
from django.db import models

from app.forms import *
from app.models import *

@login_required
@user_passes_test(lambda u: u.is_superuser)
def list(request, deposit_id=None):
    if deposit_id != None:
        d = Deposit.objects.get(pk=deposit_id)
        d.is_archive = True
        d.save()
    depositList = Deposit.objects.all()
    return render(request, 'deposit/list.html', {
        'depositList': depositList
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def all(request):
    depositList = DepositType.objects.all()
    return render(request, 'deposit/all.html', {
        'depositList': depositList
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new(request, deposit_id):
    errors = []

    depositType=DepositType.objects.get(pk=deposit_id)



    if depositType.title=='Вклад до востребования':
        F = DoVostredDepositForm


    if request.method == 'POST':
        depositForm = F(request.POST)
        if depositForm.is_valid():
            d = depositForm.save(commit=False)
            good=True
            if d.duration<=0 and depositType.title!='Вклад до востребования':
                errors.append('Срок хранения должен быть положительным')
                good = False
            if d.duration<d.pay_period and depositType.title!='Вклад до востребования':
                errors.append('Период выплат не должен привышать срок хранения')
                good = False




            if d.minimum_balance<=0 and d.is_early_withdrawal and depositType.title!='Вклад до востребования':
                errors.append('Неснижаемый остаток должен быть положительным')
                good = False
            if d.min_amount<=d.minimum_balance:
                errors.append('Неснижаемый остаток должен быть меньше минимальной суммы')
            good = False

            # elif d.depositType.title != 'Вклад до востребования' and (d.percent_for_early_withdrawal == None or d.percent_for_early_withdrawal <= 0):
            #     errors.append('percent for early withdrawal must be bigger then 0')
            # elif d.depositType.title == 'Индексируемый вклад' and d.binding_currency == None:
            #     errors.append('add binding currency')

            if good:
                #if depositType == 'Вклад до востребования':

                d.depositType =depositType
                d.save()
                return redirect('deposit:list')
    else:
        depositForm = F()

    return render(request, 'deposit/new.html', {
        'depositForm': depositForm,
        'errors': errors,
        'ID':deposit_id
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit(request, deposit_id):
    errors = []
    oldDeposit = Deposit.objects.get(pk=deposit_id)

    if request.method == 'POST':
        depositForm = DepositForm(request.POST)
        if depositForm.is_valid():
            d = depositForm.save(commit=False)
            if d.percent <= 0:
                errors.append('Percent must be bigger then 0')
            elif d.depositType.title != 'Вклад до востребования' and (d.percent_for_early_withdrawal == None or d.percent_for_early_withdrawal <= 0):
                errors.append('percent for early withdrawal must be bigger then 0')
            elif d.depositType.title == 'Индексируемый вклад' and d.binding_currency == None:
                errors.append('add binding currency')
            else:
                oldDeposit.is_archive = True
                oldDeposit.save()
                d.save()
                return redirect('deposit:list')
    else:
        depositForm = DepositForm(instance=oldDeposit)

    return render(request, 'deposit/edit.html', {
        'depositForm': depositForm,
        'errors': errors,
        'ID': deposit_id
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def info(request, deposit_id):
    return render(request, 'deposit/info.html', {
        'deposit': Deposit.objects.get(id=deposit_id)
    })

