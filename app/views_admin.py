from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory

from app.decorators import Only_Superuser_Permission
from app.views import index
from app.models import User, Message, MessageBox
from app.forms import adminfields, clientfields

from app.forms import AdminForm, MessageForm, SearchForm

from app.decorators import Only_Superuser_Permission

@login_required
@Only_Superuser_Permission
def new(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user = User.objects.create_superuser(**form.cleaned_data)
            user.save()
        return redirect(index)
    else:
        return render(request, 'admin/registration.html', {
            'form': AdminForm()
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
    Form = modelform_factory(User, fields=adminfields)
    return render(request, 'admin/info.html', {
        'form': Form(instance=request.user)
    })


@login_required
@Only_Superuser_Permission
def edit(request):
    Form = modelform_factory(User, fields=adminfields)
    user = request.user

    if request.method == 'POST':
        form = Form(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect(index)
    else:
        return render(request, 'admin/edit.html', {
            'form': Form(instance=user)
        })


@login_required
@Only_Superuser_Permission
def edit_user(request,pk):
    if not pk:
        pk=request.pk
    else:
        request.pk=pk

    Form = modelform_factory(User, fields=clientfields)
    model = User.objects.get(id=pk)

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


@Only_Superuser_Permission
@login_required
def send_message(request,pk):
    try:
        model = User.objects.get(id=pk)
    except User.DoesNotExist:
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False),'form': SearchForm(request.POST)
        })

    if request.method == 'POST':
        try:
            messageBox=MessageBox.objects.get(user_id=pk)
        except MessageBox.DoesNotExist:
            messageBox=MessageBox.objects.create(user=model)

        message=MessageForm(request.POST)
        Message.objects.create(message=message.data.get('message'),header=message.data.get('header'),
                               readed=False,messagebox=messageBox)

        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False),'form': SearchForm(request.POST)
        })
    else:
        request.pk = pk
        message = MessageForm(request.POST)
        return render(request, 'admin/sendmessage.html', {
            'form': message
        })

