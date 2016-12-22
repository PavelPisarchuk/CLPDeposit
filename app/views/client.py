# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

import app.vars as myvars
from app.forms import UserForm
from app.models import User, today


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new(request):
    if request.method == 'GET':
        return render(request, 'client/registration.html', {
            'form': UserForm()
        })
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
            errors = []
            if user.passport_date > today():
                errors.append('Неведная дата выдачи пасспорта')
            if user.get_age() < 18:
                errors.append('Пользователю не исполнилось 18')
            if user.get_age() > 150:
                errors.append('Пользователь слишком стар')
            if user.passport_date < user.birthday:
                errors.append('Неведная дата выдачи пасспорта')
            if errors:
                user.delete()
                for error in errors:
                    request.user.alert(error)
                return render(request, 'client/registration_edit.html', {
                    'form': UserForm(request.POST)
                })
            else:
                return redirect('client:list')
        else:
            if str(form.errors).find('User with this Серия already exists.'):
                request.user.alert('Пользователь с такой серией паспорта уже зарегестрирован')
            return render(request, 'client/registration_edit.html', {
                'form': UserForm(request.POST)
            })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def list(request):
    return render(request, 'client/list.html', {
        'clients': User.objects.all().filter(is_superuser=False)[0:myvars.start_client_list_load]
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
        return render(request, 'client/list_partial.html', {
            'clients': users[0:myvars.start_client_list_load]
        })
    except:
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False)[0:15]
        })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def partiallistsearch(request):
    try:
        loadcount = int(request.GET['loadcount'])
        name = request.GET['full']
        users = []
        for user in User.objects.all():
            if name.lower() in user.get_full_name().lower() and not user.is_superuser:
                users.append(user)
        users = users[loadcount:(
        loadcount + myvars.next_client_list_load) if loadcount != 0 else myvars.start_client_list_load]
        return render(request, 'client/list_partial.html', {
            'clients': users
        })
    except:
        return render(request, 'client/list_partial.html', {
            'clients': User.objects.all().filter(is_superuser=False)[0:myvars.start_client_list_load]
        })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def partiallist(request):
    try:
        loadcount = int(request.GET['loadcount'])
        users = User.objects.all().filter(is_superuser=False)[loadcount:loadcount + myvars.next_client_list_load]
        return render(request, 'client/list_partial.html', {
            'clients': users
        })
    except:
        return render(request, 'client/list_partial.html', {
            'clients': User.objects.all().filter(is_superuser=False)[0:myvars.start_client_list_load]
        })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def info(request):
    try:
        user = User.objects.get(id=request.GET['user_id'])
        return render(request, 'client/info.html', {
            'client': user
        })
    except:
        return render(request, 'client/info.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def getlistlen(request):
    return JsonResponse({'start_len': myvars.start_client_list_load, 'next_len': myvars.next_client_list_load})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def password(request, id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        user.set_password(request.POST.get("password_new"))
        user.save()
        request.user.alert('Пароль сменен успешно')
        return redirect('client:list')
    else:
        return render(request, 'client/password.html', {
            "id": id
        })
