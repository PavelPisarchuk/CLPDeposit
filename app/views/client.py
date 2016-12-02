# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from app.forms import UserForm, SearchForm
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
        'clients': User.objects.all().filter(is_superuser=False),
        'form': SearchForm()
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def search(request):
    from app.forms import SearchForm

    if(request.POST):
        users = User.objects.all()
        Form = SearchForm(request.POST)

        if(Form.data.get('first_name')):
            users = users.filter(first_name__contains=Form.data.get('first_name'))
        if(Form.data.get('last_name')):
            users = users.filter(last_name__contains=Form.data.get('last_name'))
        if(Form.data.get('passport_id')):
            users = users.filter(passport_id__contains=Form.data.get('passport_id'))

        return render(request, 'client/list.html', {
            'form': Form, 'clients': users.filter(is_superuser=False)
        })
    else:
        return redirect('client:list')

