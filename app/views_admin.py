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

    if request.method == 'POST':
        depositForm = DepositForm(request.POST)
        if depositForm.is_valid():
            depositForm.save()
            depositForm = DepositForm()
    else:
        depositForm = DepositForm()

    return render(request, 'admin/depositConfigurator.html', {'depositForm': depositForm, 'depositList':depositList})

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

