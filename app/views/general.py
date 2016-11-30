# -*- coding: utf-8 -*-
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
    from app.models import Currency, ExchangeRate
    from itertools import permutations

    exchange_rates = ExchangeRate.objects.all()
    result = []

    for date in exchange_rates.values_list('date', flat=True).distinct():
        result.append(
            [date] +
            list(map(lambda item: round(item.index, 2), exchange_rates.filter(date=date)))
        )

    return render(request, 'rates.html', {
        'headers': ['Дата'] + list(map(lambda items: "{} > {}".format(items[0].icon, items[1].icon), permutations(Currency.objects.all(), 2))),
        'data': result
    })
