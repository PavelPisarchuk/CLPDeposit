from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.views import index
from app.models import User


@login_required
def new(request):
    from app.forms import AdminForm

    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.create_superuser(username=user.username,
                                        email=user.email,
                                        password=user.password)
        return redirect(list)
    else:
        return render(request, 'admin/registration.html', {
            'form': AdminForm()
        })

@login_required
def list(request):
    return render(request, 'admin/list.html', {
        'admins': User.objects.all().filter(is_superuser=True)
    })