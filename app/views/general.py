# -*- coding: utf-8 -*-
import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.models import User


def index(request):
    return render(request, 'index.html')


def login(request):
    if (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

        return redirect('index')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('index')


@login_required
def password(request):
    try:
        if (request.method == "POST"):
            pk = request.user.id
            user = User.objects.get(id=pk)
            user.change_password(
                request.POST.get("password_old"),
                request.POST.get("password_new"),
                request.POST.get("password_new_repeat")
            )
            return redirect('logout')
        else:
            return render(request, 'password.html')
    except:
        return redirect('password')


def rates(request):
    from app.models import Currency

    rates_data = [[currency.title, currency.from_exchange_rates()] for currency in Currency.objects.all()]

    return render(request, 'rates.html', {
        'date': datetime.date.today(),
        'rates_data': rates_data
    })
