from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.views import index
from app.models import *
from app.forms import *


@login_required
def all(request):

    deposits=Deposit.objects.all()

    return render(request, 'contract/all.html', {'deposits':deposits})


@login_required
def new(request, deposit_id):

    d=Deposit.objects.filter(id=deposit_id)[0]
    dt=d.depositType

    if dt == 'Сберегательный вклад':
        F=SavingsDepositForm
    elif dt == 'Вклад до востребования':
        F=DemandDepositForm

    if request.method == 'POST':
        form = F(request.POST)
        if form.is_valid():
            contract=form.save(commit=False)
            contract.deposit=d;
            contract.save()
            return redirect('contract:list')
    else:
        form = F()

    return render(request, 'contract/new.html', {'ID':deposit_id, 'form':form, 'deposit':d})



def list(request):

    deposits=Contract.objects.all()#filter(bill__client_=request.user)

    return render(request, 'contract/list.html', {'deposits':deposits})



def info(request,deposit_id):

    #deposits=Contract.objects.all()#filter(bill__client_=request.user)

    return render(request, 'contract/info.html')