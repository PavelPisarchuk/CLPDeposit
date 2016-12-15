# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError

from app.forms import ContractForm
from app.models import Action, Bill, Deposit, Contract


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
    try:
        errors = []
        d = Deposit.objects.get(pk=deposit_id)
        if d.is_archive:
            raise Exception
        dt = d.depositType.title
        querySet = Bill.objects.filter(client=request.user, currency=d.currency, is_private=True)

        F = ContractForm

        if request.method == 'POST':
            form = F(request.POST)
            form.fields["bill"].queryset = querySet
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
                    contract.deposit_bill = bill
                    contract.deposit = d
                    contract.calculate_end_date()
                    contract.save()
                    Action.add(
                        action='Создание',
                        contract=contract,
                        money=contract.start_amount
                    )
                    return redirect('contract:list')
        else:
            form = F()
            form.fields["bill"].queryset = querySet

        return render(request, 'contract/new.html', {
            'ID': deposit_id,
            'form': form,
            'deposit': d,
            'errors': errors
        })
    except:
        return HttpResponse(status=404)

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


@login_required
def addmoney(request):
    try:
        _contract = Contract.objects.get(id=int(request.POST["contid"]))
        _bill = Bill.objects.get(id=int(request.POST['billid']))
        _money = int(request.POST['money'])
        refill_response = _contract.refill(_money, _bill)
        if refill_response[0]:
            return JsonResponse({
                'succes': True,
                'operation': 'Пополнение выполнено успешно',
                'id': _contract.id,
                'newvalue': _contract.deposit_bill.value_in_currency()
            })
        else:
            return JsonResponse({
                'succes': False,
                'errors': refill_response[1]
            })
    except:
        return JsonResponse({
            'succes': False,
            'errors': 'Что-то пошло не так , првоерьет всё и повторите запрос'
        })


@login_required
def submoney(request):
    try:
        _contract = Contract.objects.get(id=int(request.POST["contid"]))
        _money = int(request.POST['money'])
        try:
            necessarily = True if request.POST['necessarily'] == 'on' else False
        except MultiValueDictKeyError:
            necessarily = False
        withdraw_response = _contract.withdraw(_money, necessarily)
        if withdraw_response[0]:
            return JsonResponse({
                'succes': True,
                'operation': 'Снятие успешно завершено',
                'id': _contract.id,
                'newvalue': _contract.deposit_bill.value_in_currency()
            })
        else:
            return JsonResponse({
                'succes': False,
                'errors': withdraw_response[1]
            })
    except:
        return JsonResponse({
            'succes': False,
            'errors': 'Что-то пошло не так , првоерьет всё и повторите запрос'
        })


@login_required
def close(request):
    try:
        Contract.objects.get(bill__client=request.user, id=request.POST['contid']).close()
        rend = render_to_string('contract/partial_list.html', context={
            'contract': Contract.objects.get(id=request.POST['contid'])
        })
        return JsonResponse({
            'succes': True,
            'operation': 'Вклад закрыт',
            'id': request.POST['contid'],
            'render': rend
        })
    except:
        return JsonResponse({
            'succes': False,
            'errors': 'Что-то пошло не так'
        })
