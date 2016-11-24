from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.views_client import list as listpage
from app.views import index
from app.models import User, Card, Bill,Currency
from app.decorators import Only_Superuser_Permission

@login_required
def bills(request, pk=None):
    try:
        _user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return render(request, index)

    bills = Bill.objects.all().filter(client_id=_user.id).order_by('id')
    print(len(bills))
    return render(request,'bill/bills.html',{
        'bills': bills
    })

@login_required
def card(request, pk=None):
    pass

@login_required
def cards(request, pk=None):
    try:
        _user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return render(request,index)

    cards = Card.objects.all().filter(bill__client_id=_user.id).order_by('bill_id')
    return render(request, 'bill/cards.html', {
        'cards': cards
    })

@login_required
def cardsinbill(request,pk):
    try:
        _bill = Bill.objects.get(id=pk)
    except Bill.DoesNotExist:
        return render(request, index)

    _cards = Card.objects.all().filter(bill=_bill)

    return render(request, 'bill/cardsinbill.html', {
        'cards': _cards,
        'bill': _bill
    })

@Only_Superuser_Permission
@login_required
def addbill(request, pk=None):
    try:
        _user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return render(request, index)

    if request.POST:
        try:
            c = Currency.objects.get(title='BYN')
        except Currency.DoesNotExist:
            c = Currency.objects.create(title='BYN', icon='p')

        Bill.objects.create(client=_user, money=0, currency=c)
        return listpage(request)
    else:
        return render(request, 'bill/addbill.html', {
            'bill_user': _user
        })
