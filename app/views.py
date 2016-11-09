from django.shortcuts import render

def Index(request):
    context = {
    }
    return render(request, 'index.html', context)