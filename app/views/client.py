# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
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
        'clients': User.objects.all().filter(is_superuser=False)
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def search(request):
    first = request.POST['first']
    last = request.POST['last']
    father = request.POST['father']
    print '{0} {1} {2}'.format(last, first, father)
    return render(request, 'client/list_search.html', {
        'clients': User.objects.all().filter(Q(first_name__icontains=first) & Q(last_name__icontains=last) &
                                             Q(father_name__icontains=father)).filter(is_superuser=False)
    })
