from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from app.models import User, Card, Bill, Currency


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

        bill.money += int(request.POST['money'])
        bill.save()
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

        Bill.add(_user, 0, currency)#objects.create(client=_user, money=0, currency=c)
        return redirect('client:list')
    else:
        return render(request, 'bill/addbill.html', {
            'bill_user': _user
        })
