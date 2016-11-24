from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from app.views import index
from app.models import User
from app.forms import *


@login_required
def list(request):
    return render(request, 'admin/list.html', {
        'admins': User.objects.all().filter(is_superuser=True)
    })


@login_required
def info(request):
    from django.forms import modelform_factory
    from app.models import User as Model

    Form = modelform_factory(Model, fields=("username", "email"))

    return render(request, 'admin/info.html', {
        'form': Form(instance=request.user)
    })


@login_required
def edit(request):
    from django.forms import modelform_factory
    from app.models import User as Model

    Form = modelform_factory(Model, fields=("username", "email", "password"))
    model = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = Form(request.POST, instance=model)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
        return redirect(index)
    else:
        return render(request, 'admin/edit.html', {
            'form': Form(instance=model)
        })


@login_required
def new(request):
    from app.forms import AdminForm as Form

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.create_superuser(username=user.username,
                                        email=user.email,
                                        password=user.password)
        return redirect(index)
    else:
        return render(request, 'admin/registration.html', {
            'form': Form()
        })




@login_required
def DepositConfigurator(request):

    depositList=Deposit.objects.all()

    return render(request, 'admin/depositConfigurator.html', {'depositList':depositList})


@login_required
def NewDeposit(request,deposit_id):

    errors=[]

    if request.method == 'POST':
        depositForm = DepositForm(request.POST)
        if depositForm.is_valid():
            d=depositForm.save(commit=False)
            if d.percent<=0:
                errors.append('Percent must be bigger then 0')
            elif d.depositType!='Вклад до востребования' and (d.percent_for_early_withdrawal==None or d.percent_for_early_withdrawal<=0):
                errors.append('percent for early withdrawal must be bigger then 0')
            elif d.depositType=='Индексируемый вклад' and d.binding_currency==None:
                errors.append('add binding currency')
            else:
                d.save()
                return redirect('/admin/deposit_configurator/')
    else:
        depositForm = DepositForm()

    return render(request, 'admin/newDeposit.html', {'depositForm': depositForm, 'errors':errors})


@login_required
def ChangeDeposit(request,deposit_id):

    errors=[]
    oldDeposit = Deposit.objects.get(pk=deposit_id)

    if request.method == 'POST':
        depositForm = DepositForm(request.POST)
        if depositForm.is_valid():
            d=depositForm.save(commit=False)
            if d.percent<=0:
                errors.append('Percent must be bigger then 0')
            elif d.depositType!='Вклад до востребования' and (d.percent_for_early_withdrawal==None or d.percent_for_early_withdrawal<=0):
                errors.append('percent for early withdrawal must be bigger then 0')
            elif d.depositType=='Индексируемый вклад' and d.binding_currency==None:
                errors.append('add binding currency')
            else:
                oldDeposit.is_archive=True;
                oldDeposit.save()
                d.save()
                return redirect('/admin/deposit_configurator/')
    else:
        depositForm = DepositForm(instance=oldDeposit)

    return render(request, 'admin/changeDeposit.html', {'depositForm': depositForm, 'errors':errors,'ID':deposit_id})



@login_required
def NewCurrency(request):

    currencyList=Currency.objects.all()

    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            form = CurrencyForm()
    else:
        form = CurrencyForm()

    return render(request, 'admin/newCurrency.html', {'form': form, 'currencyList':currencyList})

