from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index(request):
    # from app.models import User
    # User.objects.create_superuser('admin', 'admin@admin.ru', 'admin')

    return render(request, 'index.html', {})

def login(request):
    if (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

        return redirect(index)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(index)