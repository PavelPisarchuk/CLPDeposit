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
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_superuser(**form.cleaned_data)
            user.save()
            errors = []
            if user.passport_date > today():
                errors.append('Неведная дата выдачи пасспорта')
            if user.get_age() < 18:
                errors.append('Пользователю не исполнилось 18')
            if errors:
                user.delete()
                for error in errors:
                    request.user.alert(error)
                return render(request, 'employee/registration_edit.html', {
                    'form': UserForm(request.POST)
                })
            else:
                return redirect('employee:list')
        else:
            if str(form.errors).find('User with this Серия already exists.'):
                request.user.alert('Пользователь с такой серией паспорта уже зарегестрирован')
            return render(request, 'employee/registration_edit.html', {
                'form': UserForm(request.POST)
            })


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
    contract_all = Contract.objects.all()
    if len([contract for contract in contract_all if
            contract.sign_date + relativedelta(years=1) >= today()]) > 0:

        data = [str(contract.deposit) for contract in contract_all if
                contract.sign_date + relativedelta(years=1) >= today()]
        deposit_popularity = Counter(data)

        data = [contract.deposit.currency.title for contract in contract_all if
                contract.sign_date + relativedelta(years=1) >= today()]
        currency_popularity = Counter(data)

        data = [int(contract.deposit.currency.calc(Currency.objects.get(title='BYN'), contract.start_amount)) for
                contract in contract_all if contract.sign_date + relativedelta(years=1) >= today()]
        _min = min(data)
        _max = max(data)
        step = int((_max - _min) / 10)
        if step < 1:
            step = 1

        def calculate_amount(amount):
            for val in range(_min, _max + step, step):
                if amount <= val:
                    prev = val - step
                    if prev < 0:
                        prev = 0
                    return '{0}-{1}'.format(prev, val)

        data = [x for x in (map(calculate_amount, data))]
        print(data)
        amount_popularity = Counter(data)

        return JsonResponse({
            'deposit_popularity': deposit_popularity,
            'currency_popularity': currency_popularity,
            'amount_popularity': amount_popularity
        })

    else:
        return JsonResponse({})
