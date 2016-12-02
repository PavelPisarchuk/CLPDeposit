from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.forms import EditUserForm


@login_required
def edit(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'profile/edit.html', {
            'form': EditUserForm(instance=user)
        })
    elif request.method == 'POST':
        try:
            form = EditUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                request.user.alert('Данные сохранены.')
            else:
                request.user.alert(form.errors)
        finally:
            return redirect('profile:info')


@login_required
def password(request):
    if (request.method == "POST"):
        if request.user.change_password(
                request.POST.get("password_old"),
                request.POST.get("password_new"),
                request.POST.get("password_new_repeat")
        ):
            return redirect('logout')
        else:
            request.user.alert('Текущий пароль введен неверно')
            return redirect('profile:password')
    else:
        return render(request, 'profile/password.html')


@login_required
def info(request):
    return render(request, 'profile/info.html', {
        'form': EditUserForm(instance=request.user)
    })
