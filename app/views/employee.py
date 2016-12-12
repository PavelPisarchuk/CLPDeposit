# -*- coding: utf-8 -*-
from collections import Counter

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.forms import UserForm
from app.models import *


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new(request):
    if request.method == 'GET':
        return render(request, 'employee/registration.html', {
            'form': UserForm()
        })
    elif request.method == 'POST':
        try:
            form = UserForm(request.POST)
            if form.is_valid():
                user = User.objects.create_superuser(**form.cleaned_data)
                user.save()
            else:
                request.user.alert(form.errors)
        finally:
            return redirect('employee:list')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def list(request):
    return render(request, 'employee/list.html', {
        'admins': User.objects.all().filter(is_superuser=True)
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request):
    try:
        if request.method == 'POST':
            _user = User.objects.get(id=request.POST["num"])
            oldname = _user.get_full_name()
            _user.first_name, _user.last_name, _user.father_name = request.POST["firstname"], \
                                                                   request.POST["lastname"], request.POST["fathername"]
            _user.save()
            return JsonResponse({'id': _user.id, 'newfull': _user.get_full_name(), 'newfather': _user.father_name,
                                 'newlast': _user.last_name, 'newfirst': _user.first_name, 'succes': True,
                                 'operation': 'Имя пользовталея {0} изменено на {1} успешно'.format(oldname,
                                                                                                    _user.get_full_name())})
    except Exception:
        return JsonResponse({'succes': False, 'errors': 'dsa'})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def stats(request):
    data = [contract.deposit.depositType.title for contract in Contract.objects.all() if
            contract.end_date + relativedelta(years=1) >= today()]
    deposit_popularity = Counter(data)

    data = [contract.deposit.currency.title for contract in Contract.objects.all() if
            contract.end_date + relativedelta(years=1) >= today()]
    currency_popularity = Counter(data)

    def calculate_amount(contract):
        amount = contract.deposit.currency.calc(Currency.objects.get(title='BYN'), contract.start_amount)
        if amount < 500:
            return '<500'
        elif amount < 1000:
            return '500-1000'
        elif amount < 1500:
            return '1000-1500'
        elif amount < 2000:
            return '1500-2000'
        elif amount < 2500:
            return '2000-2500'
        elif amount < 3000:
            return '2500-3000'
        elif amount < 3500:
            return '3000-3500'
        else:
            return '>3500'

    data = map(calculate_amount, [contract for contract in Contract.objects.all() if
                                  contract.end_date + relativedelta(years=1) >= today()])
    amount_popularity = Counter(data)

    return JsonResponse({'Популярность вкладов': deposit_popularity},
                        {'Популярность валют': currency_popularity},
                        {'Популярность сумм': amount_popularity}, )
