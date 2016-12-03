# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import modelform_factory
from django.shortcuts import render, redirect

from app.models import Deposit, Bill, Contract


@login_required
@user_passes_test(lambda u: not u.is_superuser)
def all(request):

    deposits = Deposit.objects.filter(is_archive=False)

    return render(request, 'contract/all.html', {
        'deposits': deposits
    })


@login_required
@user_passes_test(lambda u: not u.is_superuser)
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

            if contract.start_amount < minAmount:
                errors.append('Сумма должна быть не меньше ' + str(minAmount) + " " + str(currency))
            elif not contract.bill.pop(contract.start_amount):
                errors.append('Недостаточно средств на счету')
            else:
                bill = request.user.add_bill(d.currency,contract.start_amount,True)
                contract.deposit_bill=bill
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
@user_passes_test(lambda u: not u.is_superuser)
def list(request):
    return render(request, 'contract/list.html', {
        'contracts': request.user.get_contracts()
    })


@login_required
@user_passes_test(lambda u: not u.is_superuser)
def info(request, deposit_id):
    return render(request, 'contract/info.html', {
        'contract': Contract.objects.get(pk=deposit_id)
    })
