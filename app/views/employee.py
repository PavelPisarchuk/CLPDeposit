# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelform_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.forms import AdminForm, adminfields
from app.models import User


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new(request):
    try:
        if request.method == 'POST':
            form = AdminForm(request.POST)
            if form.is_valid():
                user = User.objects.create_superuser(**form.cleaned_data)
                user.save()
            return redirect('employee:list')
        else:
            return render(request, 'employee/registration.html', {
                'form': AdminForm()
            })
    except:
        return redirect('employee:list')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def list(request):
    return render(request, 'employee/list.html', {
        'admins': User.objects.all().filter(is_superuser=True)
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def info(request):
    Form = modelform_factory(User, fields=adminfields)
    return render(request, 'employee/info.html', {
        'form': Form(instance=request.user)
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit(request):
    Form = modelform_factory(User, fields=adminfields)
    user = request.user

    if request.method == 'POST':
        form = Form(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect('employee:info')
    else:
        return render(request, 'employee/edit.html', {
            'form': Form(instance=user)
        })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request):
    try:
        if request.method == 'POST':
            _user = User.objects.get(id=request.POST["num"])
            oldname = _user.get_full_name()
            _user.first_name, _user.last_name, _user.father_name = request.POST["firstname"], \
                                                                   request.POST["lastname"], request.POST["fathername"]
            _user.save()
            return JsonResponse({'id': _user.id, 'newfull': _user.get_full_name(), 'newfather': _user.father_name,
                                 'newlast': _user.last_name, 'newfirst': _user.first_name, 'succes': True,
                                 'operation': 'Имя пользовталея {0} изменено на {1} успешно'.format(oldname,
                                                                                                    _user.get_full_name())})
    except Exception:
        return JsonResponse({'succes': False, 'errors': 'dsa'})
