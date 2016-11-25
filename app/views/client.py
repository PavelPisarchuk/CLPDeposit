from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelform_factory
from django.shortcuts import render, redirect

from app.forms import UserForm, SearchForm, clientfields
from app.models import User


@login_required
@user_passes_test(lambda u: u.is_superuser)
def new(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
        return redirect('client:list')
    else:
        return render(request, 'client/registration.html', {
            'form': UserForm()
        })


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
            users=users.filter(first_name__contains=Form.data.get('first_name'))
        if(Form.data.get('last_name')):
            users=users.filter(last_name__contains=Form.data.get('last_name'))
        if(Form.data.get('passport_id')):
            users=users.filter(passport_id__contains=Form.data.get('passport_id'))


        return render(request, 'client/list.html', {
            'form':Form,'clients': users.filter(is_superuser=False)
        })
    else:
        return redirect('client:list')


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
        return redirect('client:info')
    else:
        return render(request, 'client/edit.html', {
            'form': Form(instance=user)
        })
