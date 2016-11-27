# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelform_factory
from django.shortcuts import render, redirect

from app.forms import AdminForm, adminfields, clientfields
from app.models import User


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user = User.objects.create_superuser(**form.cleaned_data)
            user.save()
        return redirect('employee:list')
    else:
        return render(request, 'admin/registration.html', {
            'form': AdminForm()
        })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def list(request):
    return render(request, 'admin/list.html', {
        'admins': User.objects.all().filter(is_superuser=True)
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def info(request):
    Form = modelform_factory(User, fields=adminfields)
    return render(request, 'admin/info.html', {
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
        return render(request, 'admin/edit.html', {
            'form': Form(instance=user)
        })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, pk):
    if not pk:
        pk = request.pk
    else:
        request.pk = pk

    Form = modelform_factory(User, fields=clientfields)
    model = User.objects.get(id=pk)

    if request.method == 'POST':
        form = Form(request.POST, instance=model)
        if form.is_valid():
            user = form.save(commit=False)
            model.save()
            user.save()
        return redirect('client:list')
    else:
        return render(request, 'admin/edituser.html', {
            'form': Form(instance=model)
        })
