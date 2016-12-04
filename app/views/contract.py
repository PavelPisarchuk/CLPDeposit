# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect

from app.forms import *
from app.models import Bill


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
    d = Deposit.objects.get(pk=deposit_id)
    dt = d.depositType.title
    querySet = Bill.objects.filter(client=request.user, currency=d.currency, is_private=True)

    F = ContractForm

    if request.method == 'POST':
        form = F(request.POST)
        form.fields["bill"].queryset =querySet
        if form.is_valid():
            contract = form.save(commit=False)
            good = True

            if contract.start_amount < d.min_amount:
                errors.append('Сумма должна быть не меньше ' + str(d.min_amount) + " " + str(d.currency))
                good = False
            elif not contract.bill.pop(contract.start_amount):
                errors.append('На счету (' + str(contract.bill.value_in_currency()) + ') недостаточно средств. ')
                good = False

            if good:
                bill = request.user.add_bill(d.currency, contract.start_amount, False)
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
