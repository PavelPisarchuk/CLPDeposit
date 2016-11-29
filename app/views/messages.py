# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.models import User, Message


@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_message(request):
    try:
        user = User.objects.get(id=request.POST['num'])
        if request.method == 'POST':
            user.send_message(
                message=request.POST['message'],
                header=request.POST['header']
            )
            return redirect('client:list')
    except:
        return redirect('client:list')


@login_required
def readmessage(request):
    try:
        if request.method == 'POST':
            msg = Message.objects.get(id=request.POST["num"])
            if request.user != msg.user:
                return redirect('errors:permission')
            msg.readed = True
            msg.save()
            return JsonResponse()
    except:
        return redirect('message:messages')


@login_required
def updatemsg(request):
    try:
        mymessages = Message.objects.all().filter(user=request.user, readed=False)
        if mymessages:
            return JsonResponse({'data': True, 'count': len(mymessages)})
        else:
            return JsonResponse({'data': False})
    except Exception:
        return JsonResponse({'data': False})


@login_required
def messages(request):
    try:
        mymessages = Message.objects.all().filter(user=request.user).order_by('-id')
        return render(request, 'message/messages.html', {
            'messages': mymessages
        })
    except:
        return redirect('message:messages')


@login_required
def delete(request):
    try:
        if request.POST:
            msg = Message.objects.get(id=request.POST['num'])
            if request.user != msg.user:
                return redirect('errors:permission')
            else:
                msg.delete()
                return redirect('message:messages')
    except:
        return redirect('message:messages')
