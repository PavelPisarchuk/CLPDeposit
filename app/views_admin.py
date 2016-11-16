from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.views import index
from app.models import User

from app.decorators import Only_Superuser_Permission

@login_required
@Only_Superuser_Permission
def new(request):
    from app.forms import AdminForm as Form

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.create_superuser(username=user.username,
                                        email=user.email,
                                        password=user.password)
        return redirect(index)
    else:
        return render(request, 'admin/registration.html', {
            'form': Form()
        })

@login_required
@Only_Superuser_Permission
def list(request):
    return render(request, 'admin/list.html', {
        'admins': User.objects.all().filter(is_superuser=True)
    })


@login_required
@Only_Superuser_Permission
def info(request):
    from django.forms import modelform_factory
    from app.models import User as Model

    Form = modelform_factory(Model, fields=("username", "email"))

    return render(request, 'admin/info.html', {
        'form': Form(instance=request.user)
    })


@login_required
@Only_Superuser_Permission
def edit(request):
    from django.forms import modelform_factory
    from app.models import User as Model

    Form = modelform_factory(Model, fields=("username", "email", "password"))
    model = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = Form(request.POST, instance=model)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
        return redirect(index)
    else:
        return render(request, 'admin/edit.html', {
            'form': Form(instance=model)
        })


@login_required
def edit_user(request,pk):
    from django.forms import modelform_factory
    from app.models import User as Model

    if not pk:
        pk=request.pk
    else:
        request.pk=pk

    Form = modelform_factory(Model, fields=("username", "last_name", "first_name", "father_name", "passport_id"))
    try:
        model = User.objects.get(id=pk)
    except User.DoesNotExist:
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False)
        })

    if request.method == 'POST':
        form = Form(request.POST, instance=model)
        if form.is_valid():
            user = form.save(commit=False)
            model.save()
            user.save()
        return redirect(index)
    else:
        return render(request, 'admin/edituser.html', {
            'form': Form(instance=model)
        })