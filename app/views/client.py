# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from app.forms import UserForm
from app.models import User


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new(request):
    if request.method == 'GET':
        return render(request, 'client/registration.html', {
            'form': UserForm()
        })
    elif request.method == 'POST':
        try:
            form = UserForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(**form.cleaned_data)
                user.save()
            else:
                request.user.alert(form.errors)
        finally:
            return redirect('client:list')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def list(request):
    return render(request, 'client/list.html', {
        'clients': User.objects.all().filter(is_superuser=False)[0:25]
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def search(request):
    try:
        name = request.GET['full']
        users = []
        for user in User.objects.all():
            if name.lower() in user.get_full_name().lower() and not user.is_superuser:
                users.append(user)
        return render(request, 'client/list_search.html', {
            'clients': users
        })
    except:
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False)
        })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def partiallist(request):
    try:
        name = request.GET['full']
        users = []
        loadcount = int(request.GET['loadcount'])
        if name:
            for user in User.objects.all():
                if name.lower() in user.get_full_name().lower() and not user.is_superuser:
                    users.append(user)
            user = user[loadcount:loadcount + 25]
        else:
            user = User.objects.all().filter(is_superuser=False)[loadcount:loadcount + 25]
        return render(request, 'client/list_search.html', {
            'clients': users
        })
    except:
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False)
        })
