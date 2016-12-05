# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from app.models import ExchangeRate, today
from app.models import User, Bill, Currency


@login_required
def bills(request):
    try:
        _bills = request.user.get_bills().order_by('id')
        return render(request, 'bill/bills.html', {
            'bills': _bills
        })
    except:
        return redirect('index')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def addonbill(request):
    if request.method == 'POST':
        try:
            bill = Bill.objects.get(id=request.POST["num"])
            pushmoney = int(request.POST['money'])
            _currency = Currency.objects.get(id=request.POST["currency"])
            if _currency != bill.currency:  # ??!!
                to_currency = ExchangeRate.objects.get(
                    to_currency=bill.currency,
                    from_currency=_currency,
                    date=today()
                )
                pushmoney = to_currency.calc(pushmoney)
            bill.push(pushmoney)
            return JsonResponse({'succes': True,
                                 'operation': 'Пополнение счёта {0} для {1} на {2} выполнено'.format(bill.id,
                                                                                                     bill.client.get_full_name(),
                                                                                                     pushmoney)})
        except MultiValueDictKeyError:
            return JsonResponse({'succes': False, 'errors': 'Введены не все поля'})
        except Currency.DoesNotExist:
            return JsonResponse({'succes': False, 'errors': 'Такой валюты нет'})
        except Exception:
            return JsonResponse({'succes': False, 'errors': 'Возникли проблемы, проверьте всё и повторите запрос'})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addbill(request):
    if request.method == 'POST':
        try:
            _user = User.objects.get(id=request.POST["num"])
            _currency = Currency.objects.get_or_create(id=request.POST["currency"])[0]
            _bill = _user.add_bill(currency=_currency, money=0, is_private=True)
            return JsonResponse({'succes': True, 'operation': 'Добавление счёта {0} для {1} выполнено'.format(_bill.id,
                                                                                                              _bill.client.get_full_name())})
        except Exception:
            return JsonResponse({'succes': False, 'errors': 'Возникли проблемы, проверьте всё и повторите запрос'})


@login_required
def billtransact(request):
    if request.POST:
        try:
            _from = int(request.POST["from"])
            _to = int(request.POST["to"])

            frombill = Bill.objects.get(id=_from)
            tobill = Bill.objects.get(id=_to)

            if frombill == tobill:
                return JsonResponse({'succes': False, 'errors': 'Перевод в тот же самый счёт невозможен!'})

            if frombill.client != request.user or tobill.client != request.user:
                return JsonResponse({'succes': False, 'errors': 'Перевод невозможен, один из счетов не ваш !'})

            else:
                _money = int(request.POST["money"])
                _currency = Currency.objects.get(id=request.POST["currency"])

                if _currency != frombill.currency or _currency != tobill.currency or frombill.currency != tobill.currency:  # ??!!
                    to_currency = ExchangeRate.objects.get(
                        to_currency=tobill.currency,
                        from_currency=_currency,
                        date=today()
                    )
                    _money = to_currency.calc(_money)

                if frombill.transfer(tobill, _money):
                    return JsonResponse({'succes': True,
                                         'operation': 'Переведено из счёта № {0} {1} на счёт № {2} !'.format(_from,
                                                                                                             _money,
                                                                                                             _to)})
                else:
                    return JsonResponse({'succes': False, 'errors': 'Недостаточно средств!'})

        except MultiValueDictKeyError:
            return JsonResponse({'succes': False, 'errors': 'Введены не все поля'})
        except Bill.DoesNotExist:
            return JsonResponse({'succes': False, 'errors': 'Такого счёта нет'})
        except Currency.DoesNotExist:
            return JsonResponse({'succes': False, 'errors': 'Такой валюты нет'})
        except Exception:
            return JsonResponse({'succes': False, 'errors': 'Возникли проблемы, проверьте всё и повторите запрос'})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def getuserbills(request):
    try:
        _user = User.objects.get(id=request.GET['num'])
        _bills = _user.get_bills()
        _bills_id = [a.id for a in _bills]
        if _bills:
            return JsonResponse({'bills': _bills_id})
        else:
            return JsonResponse({'bills': []})
    except Exception:
        return JsonResponse({'bills': []})


@login_required
def getuserbillsfromuser(request):
    try:
        _user = User.objects.get(id=request.user.id)
        _bills = _user.get_bills()
        _bills_id, _bills_money = [], []
        for a in _bills:
            _bills_id.append(a.id)
            _bills_money.append(' (  {0} {1}  )'.format(a.money, a.currency.title))
        if _bills and _user == request.user:
            return JsonResponse({'bills': _bills_id, 'money': _bills_money})
        else:
            return JsonResponse({'bills': []})
    except Exception:
        return JsonResponse({'bills': []})

@login_required
def getcurrency(request):
    try:
        _currency = Currency.objects.all()
        _currencyname = [a.title for a in _currency]
        _currency = [a.id for a in _currency]
        if _currency:
            return JsonResponse({'currency': _currency, 'currencyname': _currencyname})
        else:
            return JsonResponse({'currency': [], 'currencyname': []})
    except Exception:
        return JsonResponse({'currency': [], 'currencyname': []})
