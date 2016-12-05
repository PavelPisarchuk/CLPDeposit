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
            if not request.POST['header']:
                return JsonResponse({'succes': False, 'errors': 'Пустой заголовок !'})
            user.send_message(
                message=request.POST['message'],
                header=request.POST['header']
            )
            return JsonResponse(
                {'succes': True, 'operation': 'Сообщение для {0} отправлено'.format(user.get_full_name())})
    except Exception:
        return JsonResponse({'succes': False, 'errors': ''})


@login_required
def readmessage(request):
    try:
        if request.method == 'POST':
            msg = Message.objects.get(id=request.POST["message_id"], user=request.user)
            msg.read()
            return JsonResponse({})
    except:
        return JsonResponse({})

@login_required
def messages(request):
    try:
        return render(request, 'message/messages.html', {
            'messages': request.user.get_messages().order_by('-id')
        })
    except:
        return redirect('index')


@login_required
def delete(request):
    try:
        if request.POST:
            Message.objects.get(
                id=request.POST['message_id'],
                user=request.user
            ).delete()
            return JsonResponse({'succes': True, 'msgid': request.POST['message_id']})
    except:
        return JsonResponse({'succes': False, 'errors': 'Недостаточно прав !'})
