# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.models import ExchangeRate, today
from app.models import User, Card, Bill, Currency


@login_required
@user_passes_test(lambda u: u.is_superuser)
def addcard(request):
    if request.method == 'POST':
        try:
            bill = Bill.objects.get(id=request.POST["num"])
            bill.add_card(limit=request.POST['limit'])
            return JsonResponse({'succes': True,
                                 'operation': 'Добавление карточки к счёту {0} для {1} выполнено'.format(bill.id,
                                                                                                         bill.client.get_full_name())})
        except Exception:
            return JsonResponse({'succes': False, 'errors': 'Возникли проблемы, проверьте всё и повторите запрос'})

@login_required
def cardsinbill(request):
    try:
        _bill = Bill.objects.get(id=request.GET['num'])
        _cards = Card.objects.all().filter(bill=_bill)
        cards, limits = [], []
        for i in _cards:
            cards.append(i.id)
            limits.append(i.limit)
        return JsonResponse({'limits': limits, 'cards': cards})
    except Exception:
        return JsonResponse()


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
        except Exception:
            return JsonResponse({'succes': False, 'errors': 'Возникли проблемы, проверьте всё и повторите запрос'})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addbill(request):
    if request.method == 'POST':
        try:
            _user = User.objects.get(id=request.POST["num"])
            currency = Currency.objects.get_or_create(title='BYN')[0]
            _bill = _user.add_bill(currency=currency, money=0, is_private=True)
            return JsonResponse({'succes': True, 'operation': 'Добавление счёта {0} для {1} выполнено'.format(_bill.id,
                                                                                                              _bill.client.get_full_name())})
        except Exception:
            return JsonResponse({'succes': False, 'errors': 'dsa'})


@login_required
def billtransact(request):
    if request.POST:
        try:
            _from = int(request.POST["from"])
            _to = int(request.POST["to"])

            frombill = Bill.objects.get(id=_from)
            tobill = Bill.objects.get(id=_to)

            if frombill == tobill:
                return JsonResponse({'succes': False, 'errors': 'Перевод в тот же самый счёт !'})

            if frombill.client != request.user or tobill.client != request.user:
                return JsonResponse({'succes': False, 'errors': 'Перевод невозможен !'})

            else:
                _money = int(request.POST["money"])
                if frombill.transfer(tobill, _money):
                    return JsonResponse({'succes': True,
                                         'operation': 'Переведено из счёта № {0} {1} на счёт № {2} !'.format(_from,
                                                                                                             _money,
                                                                                                             _to)})
                else:
                    return JsonResponse({'succes': False, 'errors': 'Недостаточно средств!'})

        except:
            return JsonResponse({'succes': False, 'errors': 'Неизвестная ошибка'})

    else:
        return render(request, 'bill/billtransact.html', {
            'bills': request.user.get_bills()
        })


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
        _bills = Bill.objects.all().filter(client=_user)
        _bills_id = []
        for a in _bills:
            _bills_id.append(a.id)
        if _bills:
            return JsonResponse({'bills': _bills_id})
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
