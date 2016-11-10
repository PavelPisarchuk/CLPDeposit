from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.views import index
from app.models import User


@login_required
def new(request):
    from app.forms import UserForm

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.create_user(username = user.username,
                                     password = user.password,
                                     last_name = user.last_name,
                                     first_name = user.first_name,
                                     father_name = user.father_name)
            return redirect(index)
    else:
        return render(request, 'client/registration.html', {
            'form': UserForm()
        })


@login_required
def list(request):
    return render(request, 'client/list.html', {
        'clients': User.objects.all().filter(is_superuser=False)
    })


@login_required
def info(request):
    return