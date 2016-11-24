from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.views import index
from app.models import *
from app.forms import *


@login_required
def new(request):
    from app.forms import UserForm as Form

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.create_user(username=user.username,
                                     password=user.password,
                                     last_name=user.last_name,
                                     first_name=user.first_name,
                                     father_name=user.father_name)
        return redirect(index)
    else:
        return render(request, 'client/registration.html', {
            'form': Form()
        })

@login_required
def list(request):
    return render(request, 'client/list.html', {
        'clients': User.objects.all().filter(is_superuser=False)
    })


@login_required
def info(request):
    from django.forms import modelform_factory
    from app.models import User as Model

    Form = modelform_factory(Model, fields=("last_name", "first_name", "father_name", "passport_id", "address", "birthday", "phone"))

    return render(request, 'client/info.html', {
        'form': Form(instance=request.user)
    })


@login_required
def edit(request):
    from django.forms import modelform_factory
    from app.models import User as Model

    Form = modelform_factory(Model, fields=("last_name", "first_name", "father_name", "address", "phone", "password"))
    model = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = Form(request.POST, instance=model)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
        return redirect(index)
    else:
        return render(request, 'client/edit.html', {
            'form': Form(instance=model)
        })


@login_required
def allDeposits(request):

    deposits=Deposit.objects.all()

    return render(request, 'client/allDeposits.html', {'deposits':deposits})


@login_required
def newDeposit(request, deposit_id):

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
            return redirect('/client/myDeposits/')
    else:
        form = F()

    return render(request, 'client/newDeposit.html', {'ID':deposit_id, 'form':form, 'deposit':d})


def myDeposits(request):

    deposits=Contract.objects.all()#filter(bill__client_=request.user)

    return render(request, 'client/myDeposits.html', {'deposits':deposits})