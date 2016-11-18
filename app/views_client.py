from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory

from app.decorators import Only_Superuser_Permission
from app.views import index
from app.models import User
from app.forms import UserForm, clientfields


@login_required
@Only_Superuser_Permission
def new(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
        return redirect(index)
    else:
        return render(request, 'client/registration.html', {
            'form': UserForm()
        })

        
@login_required
@Only_Superuser_Permission
def list(request):
    return render(request, 'client/list.html', {
        'clients': User.objects.all().filter(is_superuser=False)
    })


@login_required
def info(request):
    Form = modelform_factory(User, fields=clientfields)
    return render(request, 'client/info.html', {
        'form': Form(instance=request.user)
    })


@login_required
def edit(request):
    Form = modelform_factory(User, fields=clientfields)
    user = request.user

    if request.method == 'POST':
        form = Form(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect(index)
    else:
        return render(request, 'client/edit.html', {
            'form': Form(instance=user)
        })