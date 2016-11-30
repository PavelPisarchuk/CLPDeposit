# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.forms import modelform_factory

from app.forms import *
from app.models import *


@login_required
def all(request):

    deposits = Deposit.objects.filter(is_archive=False)

    return render(request, 'contract/all.html', {
        'deposits': deposits
    })


@login_required
def new(request, deposit_id):

    errors = []
    d = Deposit.objects.filter(id=deposit_id)[0]
    dt = d.depositType
    querySet=Bill.objects.filter(client=request.user, currency=d.currency)

    if dt == 'Сберегательный вклад':
        F = modelform_factory(Contract, exclude=("is_prolongation",), )
    else:
        F = modelform_factory(Contract, exclude=(),)

    if request.method == 'POST':
        form = F(request.POST)
        form.fields["bill"].queryset =querySet
        if form.is_valid():
            contract = form.save(commit=False)
            deposit = Deposit.objects.get(pk=deposit_id)
            minAmount = deposit.min_amount
            currency = deposit.currency



            if contract.deposit_bill < minAmount:
                errors.append('Сумма должна быть не меньше ' + str(minAmount) + " " + str(currency))
            elif not contract.bill.pop(contract.deposit_bill):
                errors.append('Недостаточно средств на счету')
            else:
                contract.deposit = d
                contract.calculate_end_date()
                contract.save()
                return redirect('contract:list')
    else:
        form = F()
        form.fields["bill"].queryset =querySet

    return render(request, 'contract/new.html', {
        'ID': deposit_id,
        'form': form,
        'deposit': d,
        'errors': errors
    })


@login_required
def list(request):

    deposits = Contract.objects.filter(bill__client=request.user)

    return render(request, 'contract/list.html', {
        'deposits': deposits
    })


@login_required
def info(request, deposit_id):

    contract = Contract.objects.get(pk=deposit_id)

    return render(request, 'contract/info.html', {
        'contract': contract
    })
