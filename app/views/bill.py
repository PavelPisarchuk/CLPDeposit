#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from app.models import User, Card, Bill, Currency, Action, ActionType


@login_required
def card(request, pk=None):
    pass


@login_required
@user_passes_test(lambda u: u.is_superuser)
def addcard(request, pk=None):
    if request.POST:
        try:
            pk = request.POST["num"]
            bill = Bill.objects.get(id=pk)
        except Bill.DoesNotExist:
            return redirect('index')

        Card.objects.create(bill=bill, limit=request.POST['limit'])
        return redirect('client:list')
    else:
        try:
            _user = User.objects.get(id=pk)
        except Bill.DoesNotExist:
            return redirect('index')
        _bills = Bill.objects.all().filter(client=_user)
        if _bills:
            return render(request, 'bill/addcard.html', {
                'bills': _bills
            })
        else:
            return addbill(request,pk)


@login_required
def cards(request):
    try:
        _user = request.user
    except User.DoesNotExist:
        return redirect('index')

    cards = Card.objects.all().filter(bill__client_id=_user.id).order_by('bill_id')
    return render(request, 'bill/cards.html', {
        'cards': cards
    })


@login_required
def cardsinbill(request, pk):
    try:
        _bill = Bill.objects.get(id=pk)
    except Bill.DoesNotExist:
        return redirect('index')

    _cards = Card.objects.all().filter(bill=_bill)

    return render(request, 'bill/cardsinbill.html', {
        'cards': _cards,
        'bill': _bill
    })


@login_required
def bills(request):
    try:
        _user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return redirect('index')

    bills = Bill.objects.all().filter(client_id=_user.id).order_by('id')

    return render(request, 'bill/bills.html', {
        'bills': bills
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def addonbill(request, pk=None):
    if request.POST:
        try:
            pk = request.POST["num"]
            bill = Bill.objects.get(id=pk)
        except Bill.DoesNotExist:
            return redirect('client:list')

        pushmoney=int(request.POST['money'])
        bill.push(pushmoney)
        Action.add('FILL',None,bill,pushmoney)
        return redirect('client:list')
    else:
        try:
            _user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return redirect('client:list')
        _bills = Bill.objects.all().filter(client=_user)
        if _bills:
            return render(request, 'bill/addonbill.html', {
                'bills': _bills
            })
        else:
            return addbill(request,pk)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def addbill(request, pk=None):
    try:
        _user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return redirect('client:list')

    if request.POST:
        try:
            currency = Currency.objects.get(title='BYN')
        except Currency.DoesNotExist:
            currency = Currency.objects.create(title='BYN', icon='p')

        _bill=Bill.add(_user, 0, currency)
        Action.add('CREATE', None, _bill, 0)
        return redirect('client:list')
    else:
        return render(request, 'bill/addbill.html', {
            'bill_user': _user
        })

@login_required
def billoperations(request, pk=None):
    try:
        bill = Bill.objects.get(id=pk)
    except Bill.DoesNotExist:
        return redirect('bill:bills')

    if bill.client!=request.user:
        return redirect('errors:error')
    else:
        _operations=Action.objects.all().filter(bill=bill).order_by('-id')
        return render(request,'bill/billoperations.html',{'operations':_operations})


@login_required
def billtransact(request):
    if request.POST:
        try:
            _from =int(request.POST["_from"])
            _to = int(request.POST["_to"])

            frombill = Bill.objects.get(id=_from)
            tobill = Bill.objects.get(id=_to)

            if frombill==tobill:
                return render(request, 'bill/billtransact.html',
                              {'bills': Bill.objects.all().filter(client=request.user)})

            if frombill.client!=request.user or tobill.client!=request.user:
                return render(request, 'errors/error.html', {'errors': u'Что-то пошло не так'})
            else:
                _money = int(request.POST["money"])
                if _money<frombill.money:

                    frombill.pop(_money)
                    tobill.push(_money)

                    Action.add('TAKE_PART', None, frombill, _money)
                    Action.add('FILL', None, tobill, _money)
                    return redirect('bill:bills')
                else:
                    return render(request, 'errors/error.html',{'errors':u'Недостаточно средств'})

        except:
            return render(request, 'errors/error.html', {'errors': u'Что-то пошло не так'})


    else:
        return render(request,'bill/billtransact.html',
                      {'bills':Bill.objects.all().filter(client=request.user)})