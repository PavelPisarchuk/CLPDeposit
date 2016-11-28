# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


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
    if (request.method == "POST"):
        user = request.user
        if user.check_password(request.POST.get("password_old")):
            password_new = request.POST.get("password_new")
            password_new_repeat = request.POST.get("password_new_repeat")
            if password_new == password_new_repeat:
                user.set_password(password_new)
                user.save()
                return logout(request)
        return redirect('index')
    else:
        return render(request, 'password.html')


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
