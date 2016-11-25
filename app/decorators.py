from django.shortcuts import render


def Only_Superuser_Permission(func):
    def fun(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, 'errors/permissionerror.html')
        else:
            return func(request, *args, **kwargs)
    return fun