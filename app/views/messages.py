# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.models import User, Message


@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_message(request):
    try:
        if request.method == 'POST':
            user = User.objects.get(id=request.POST['num'])
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
            msg.read()
            return JsonResponse()
    except:
        return redirect('message:messages')


@login_required
def updatemsg(request):
    try:
        count = request.user.get_unread_messages_count()
        if count:
            return JsonResponse({'data': count, 'count': count})
        else:
            raise
    except Exception:
        return JsonResponse({'data': False})


@login_required
def messages(request):
    try:
        return render(request, 'message/messages.html', {
            'messages': request.user.get_messages().order_by('-id')
        })
    except:
        return redirect('message:messages')


@login_required
def delete(request):
    try:
        if request.POST:
            Message.objects.get(
                id=request.POST['num'],
                user=request.user
            ).delete()
            return redirect('message:messages')
    except:
        return redirect('errors:permission')
