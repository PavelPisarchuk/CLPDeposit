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

        deposit_data, currency_data, amount_data = [[str(contract.deposit), contract.deposit.currency.title,
                                                     int(contract.deposit.currency.calc(
                                                         Currency.objects.get(title='BYN'), contract.start_amount))]
                                                    for contract in Contract.objects.all() if
                                                    contract.sign_date + relativedelta(years=1) >= today()]

        deposit_popularity = Counter(deposit_data)
        currency_popularity = Counter(currency_data)

        _min = min(amount_data)
        _max = max(amount_data)
        step = int((_max - _min) / 5)
        if step < 1:
            step = 1

        def calculate_amount(amount):
            for val in range(_min, _max + step, step):
                prev = val - step
                if prev < 0:
                    prev = 0
                if (amount < val) or (amount == _max and amount <= val):
                    return '{0}-{1}'.format(prev, val)

        amount_data = [x for x in (map(calculate_amount, amount_data))]
        amount_popularity = Counter(amount_data)

        return JsonResponse({'Статистика': [
            {'Популярность вкладов': deposit_popularity},
            {'Популярность валют вкладов': currency_popularity},
            {'Популярность сумм вкладов': amount_popularity},
            # {'Популярность сумм вкладов': bad_deposit}
        ]})
        formatter = lambda dict: [{'label': key, 'y': value} for key, value in dict.items()]
        return JsonResponse({
            'deposit_popularity': formatter(deposit_popularity),
            'currency_popularity': formatter(currency_popularity),
            'amount_popularity': formatter(amount_popularity)
        })

    else:
        return JsonResponse({})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def statistics(request):
    return render(request, 'employee/statistics.html')