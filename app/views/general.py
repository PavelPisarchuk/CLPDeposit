# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.shortcuts import render, redirect

from app.management.commands import jump_day


def index(request):
    return render(request, 'index.html')


def login(request):
    if (request.method == "GET"):
        return render(request, 'login.html')
    if (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
        else:
            return redirect('login')

        return redirect('index')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


def jump(request, count):
    for _ in range(int(count)):
        jump_day.Command().handle()
    return redirect('index')


def load(request):
    call_command('loaddata', '100/users', app_label='app')
    call_command('loaddata', '100/bill', app_label='app')
    call_command('loaddata', '100/contract', app_label='app')
    return redirect('index')
