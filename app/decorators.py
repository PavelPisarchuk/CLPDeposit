from app import models
from django.shortcuts import render, redirect
from app.views import index

def Only_Superuser_Permission(func):
    def fun(request,pk=None):
        if not request.user.is_superuser:
            return render(request, 'errors/permissionerror.html')
        else:
            if pk==None:
                return func(request)
            else:
                return func(request,pk)
    return fun