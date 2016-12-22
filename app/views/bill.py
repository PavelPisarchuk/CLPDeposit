# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from app.models import User, Bill, Currency, Contract


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
            bill = Bill.objects.get(id=int(request.POST["num"]))
            pushmoney = float(request.POST['money'])
            _currency = Currency.objects.get(id=request.POST["currency"])
            pushmoney = _currency.calc(bill.currency, pushmoney)
            bill.push(pushmoney)
            return JsonResponse({
                'succes': True,
                'operation': 'Пополнение счёта {0} для {1} на {2}{3} выполнено'.format(
                    bill.id,
                    bill.client.get_full_name(),
                    "%.2f" % pushmoney,
                    bill.currency.title
                )
            })
        except MultiValueDictKeyError:
            return JsonResponse({
                'succes': False,
                'errors': 'Введены не все поля'
            })
        except Currency.DoesNotExist:
            return JsonResponse({
                'succes': False,
                'errors': 'Такой валюты нет'
            })
        except Exception:
            return JsonResponse({
                'succes': False,
                'errors': 'Возникли проблемы, проверьте всё и повторите запрос'
            })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addbill(request):
    if request.method == 'POST':
        try:
            _user = User.objects.get(id=int(request.POST["num"]))
            _currency = Currency.objects.get_or_create(id=int(request.POST["currency"]))[0]
            _bill = _user.add_bill(currency=_currency, money=0, is_private=True)
            return JsonResponse({
                'succes': True,
                'operation': 'Добавление счёта {0} для {1} выполнено'.format(
                    _bill.id,
                    _bill.client.get_full_name()
                )
            })
        except Exception:
            return JsonResponse({
                'succes': False,
                'errors': 'Возникли проблемы, проверьте всё и повторите запрос'
            })


@login_required
def billtransact(request):
    if request.POST:
        try:
            _from = int(request.POST["from"])
            _to = int(request.POST["to"])

            frombill = Bill.objects.get(id=_from)
            tobill = Bill.objects.get(id=_to)

            if frombill == tobill:
                return JsonResponse({
                    'succes': False,
                    'errors': 'Перевод в тот же самый счёт невозможен!'
                })

            if frombill.client != request.user or tobill.client != request.user:
                return JsonResponse({
                    'succes': False,
                    'errors': 'Перевод невозможен, один из счетов не ваш !'
                })

            else:
                _money = float(request.POST["money"])
                _currency = Currency.objects.get(id=int(request.POST["currency"]))

                if frombill.transfer(tobill, _money, _currency):
                    return JsonResponse({
                        'succes': True,
                        'operation': 'Переведено из счёта № {0} {1}{3} на счёт № {2} !'.format(
                            _from,
                            "%.2f" % (_money),
                            _to,
                            _currency.title
                        ),
                        'from': [frombill.id, "%.2f" % frombill.money],
                        'to': [tobill.id, "%.2f" % tobill.money]
                    })
                else:
                    return JsonResponse({
                        'succes': False,
                        'errors': 'Недостаточно средств!'
                    })

        except MultiValueDictKeyError:
            return JsonResponse({
                'succes': False,
                'errors': 'Введены не все поля'
            })
        except Bill.DoesNotExist:
            return JsonResponse({
                'succes': False,
                'errors': 'Такого счёта нет'
            })
        except Currency.DoesNotExist:
            return JsonResponse({
                'succes': False,
                'errors': 'Такой валюты нет'
            })
        except Exception:
            return JsonResponse({
                'succes': False,
                'errors': 'Возникли проблемы, проверьте всё и повторите запрос'
            })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def getuserbills(request):
    try:
        _user = User.objects.get(id=int(request.GET['num']))
        _bills = _user.get_bills()
        _bills_id, _bills_info = [], []
        for a in _bills:
            _bills_id.append(a.id)
            _bills_info.append('{2} (  {0} {1}  )'.format("%.2f" % a.money, a.currency.title, a.id))
        if _bills:
            return JsonResponse({
                'bills': _bills_id,
                'billsinfo': _bills_info
            })
        else:
            return JsonResponse({
                'bills': []
            })
    except Exception:
        return JsonResponse({
            'bills': []
        })


@login_required
def getuserbillsfromuser(request):
    try:
        _user = User.objects.get(id=int(request.user.id))
        _bills = _user.get_bills()
        _bills_id, _bills_money = [], []
        for a in _bills:
            _bills_id.append(a.id)
            _bills_money.append(' (  {0} {1}  )'.format("%.2f" % a.money, a.currency.title))
        if _bills and _user == request.user:
            return JsonResponse({'bills': _bills_id, 'money': _bills_money})
        else:
            return JsonResponse({
                'bills': []
            })
    except Exception:
        return JsonResponse({
            'bills': []
        })

@login_required
def getcurrency(request):
    try:
        _currency = Currency.objects.all()
        _currencyname = [a.title for a in _currency]
        _currency = [a.id for a in _currency]
        if _currency:
            return JsonResponse({
                'currency': _currency,
                'currencyname': _currencyname
            })
        else:
            return JsonResponse({
                'currency': [],
                'currencyname': []
            })
    except Exception:
        return JsonResponse({
            'currency': [],
            'currencyname': []
        })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def userbillinfo(request):
    try:
        user = User.objects.get(id=int(request.GET['user_id']))
        contracts, bills = user.get_contracts(), user.get_bills()
        return render(request, 'bill/bills_info.html', {
            'bills': bills,
            'contracts': contracts
        })
    except:
        return render(request, 'bill/bills_info.html')


@login_required
def usercontracts(request):
    try:
        return render(request, 'bill/user_contracts.html', {
            'contracts': User.objects.get(id=request.user.id).get_contracts().filter(bill_id=request.GET['billid'])
        })
    except:
        return render(request, 'bill/user_contracts.html', {
            'contracts': {}
        })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def closebill(request):
    try:
        if request.method == 'POST':
            _bill = Bill.objects.get(id=int(request.POST['num']))
            _reason = request.POST['reason']
            if not Contract.objects.all().filter(bill=_bill, is_act=True):
                if _bill.money < 0.01:
                    _client, billinfo = _bill.client, ' №{0} Валюта:{1}'.format(_bill.id, _bill.currency.title)
                    _bill.delete()
                    _client.send_message('Удаление счёта',
                                         'Ваш счёт ' + billinfo + '  был удалён. Причина:' + _reason + ' .')
                    return JsonResponse({
                        'succes': True,
                        'operation': 'Удаление счёта выполнено успешно'
                    })
                else:
                    return JsonResponse({
                        'succes': False,
                        'errors': 'Невозможно удалить счёт, баланс больше или равен 0.01'
                    })
            else:
                return JsonResponse({
                    'succes': False,
                    'errors': 'Невозможно удалить счёт, имеются депозиты привязанные к данному счёту'
                })
    except:
        return JsonResponse({
            'succes': False,
            'errors': 'Возникли проблемы, проверьте всё и повторите запрос'
        })
