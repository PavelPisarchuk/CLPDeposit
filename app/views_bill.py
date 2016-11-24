from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from app.views import index
from app.models import User,Card,Bill
from app.forms import UserForm

@login_required
def cards(request,pk=None):
    try:
        _user=User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return render(request,index)

    cards=Card.objects.all().filter(bill__client_id=_user.id).order_by('bill_id')
    return render(request, 'bill/cards.html', {'cards':cards})

@login_required
def cardsinbill(request,pk):
    try:
        _bill=Bill.objects.get(id=pk)
    except Bill.DoesNotExist:
        return render(request,index)

    _cards=Card.objects.all().filter(bill=_bill)

    return render(request,'bill/cardsinbill.html',{'cards':_cards,'bill':_bill})

