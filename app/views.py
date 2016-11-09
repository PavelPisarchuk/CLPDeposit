from django.shortcuts import render, redirect
from django.contrib import auth


def index(request):
    context = {
    }
    return render(request, 'index.html', context)

def login(request):
    if (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

        return redirect(index)

def logout(request):
    auth.logout(request)
    return redirect(index)