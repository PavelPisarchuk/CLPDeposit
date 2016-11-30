# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


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
            request.user.change_password(
                request.POST.get("password_old"),
                request.POST.get("password_new"),
                request.POST.get("password_new_repeat")
            )
            return redirect('logout')
        else:
            return render(request, 'password.html')
    except:
        return redirect('password')
