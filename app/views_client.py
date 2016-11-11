from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.views import index
from app.models import User


@login_required
def new(request):
    from app.forms import UserForm as Form

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.create_user(username=user.username,
                                     password=user.password,
                                     last_name=user.last_name,
                                     first_name=user.first_name,
                                     father_name=user.father_name)
        return redirect(index)
    else:
        return render(request, 'client/registration.html', {
            'form': Form()
        })


@login_required
def list(request):
    return render(request, 'client/list.html', {
        'clients': User.objects.all().filter(is_superuser=False)
    })


@login_required
def info(request):
    from django.forms import modelform_factory
    from app.models import User as Model
    form = modelform_factory(Model, fields=("last_name", "first_name", "father_name", "passport_id"))
    return render(request, 'client/info.html', {
        'form': form(instance=request.user)
    })


@login_required
def edit(request):
    from app.forms import UserForm as Form

    model = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = Form(request.POST, instance=model)
        if form.is_valid():
            form.save()
        return redirect(index)
    else:
        return render(request, 'client/edit.html', {
            'form': Form(instance=model)
        })