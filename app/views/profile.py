# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from app.forms import EditUserForm
from app.models import today, User


@login_required
def edit(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'profile/edit.html', {
            'form': EditUserForm(instance=user)
        })

    elif request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            errors = []
            if user.passport_date > today():
                errors.append('Дата выдачи паспорта из будущего')
            if user.get_age() < 18:
                errors.append('Пользователю не исполнилось 18')
            if user.get_age() > 150:
                errors.append('Пользователь слишком стар')
            if user.passport_date < user.birthday:
                errors.append('Паспорт выдан до рождения')
            if errors:
                for error in errors:
                    request.user.alert(error)
                return render(request, 'profile/edit.html', {
                    'form': EditUserForm(request.POST)
                })
            else:
                form.save()
                request.user.alert('Данные сохранены.')
                return redirect('profile:info')
        else:
            err = str(form.errors) + ""
            if err.find('phone') >= 0:
                request.user.alert('Пользователь с таким номером телефона уже зарегестрирован')
            if err.find('passport_id') >= 0:
                request.user.alert('Пользователь с таким номером паспорта уже зарегестрирован')
            if err.find('passport_ser') >= 0:
                request.user.alert('Пользователь с такой серией паспорта уже зарегестрирован')
            if err.find('username') >= 0:
                request.user.alert('Пользователь с таким логином уже зарегестрирован')
            return render(request, 'profile/edit.html', {
                'form': EditUserForm(request.POST)
            })


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
@user_passes_test(lambda u: u.is_superuser)
def setpassword(request, id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        user.set_password(request.POST.get("password_new"))
        user.save()
        request.user.alert('Пароль сменен успешно')
        return redirect('client:list')
    else:
        return render(request, 'client/../../templates/profile/set_password.html', {
            "id": id
        })


@login_required
def info(request):
    return render(request, 'profile/info.html', {
        'form': EditUserForm(instance=request.user)
    })
