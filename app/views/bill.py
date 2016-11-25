from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render

from app.decorators import Only_Superuser_Permission
from app.forms import SearchForm
from app.models import User, Card, Bill,Currency
from app.views.general import index
from app.views.client import list


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
            return index

        Card.objects.create(bill=bill, limit=request.POST['limit'])
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False),
            'form': SearchForm()
        })

    else:
        try:
            _user = User.objects.get(id=pk)
        except Bill.DoesNotExist:
            return render(request, index)
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
        return render(request,index)

    cards = Card.objects.all().filter(bill__client_id=_user.id).order_by('bill_id')
    return render(request, 'bill/cards.html', {
        'cards': cards
    })


@login_required
def cardsinbill(request, pk):
    try:
        _bill = Bill.objects.get(id=pk)
    except Bill.DoesNotExist:
        return render(request, index)

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
        return render(request, index)

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
            return index

        bill.money += int(request.POST['money'])
        bill.save()
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False),
            'form': SearchForm()
        })
    else:
        try:
            _user = User.objects.get(id=pk)
        except Bill.DoesNotExist:
            return render(request,index)
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
        return render(request, index)

    if request.POST:
        try:
            c = Currency.objects.get(title='BYN')
        except Currency.DoesNotExist:
            c = Currency.objects.create(title='BYN', icon='p')

        Bill.add(_user,0,c)#objects.create(client=_user, money=0, currency=c)
        return list(request)
    else:
        return render(request, 'bill/addbill.html', {
            'bill_user': _user
        })
