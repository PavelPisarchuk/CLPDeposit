from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.forms import MessageForm
from app.models import User, Message


@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_message(request, pk):
    try:
        model = User.objects.get(id=pk)
    except User.DoesNotExist:
        return redirect('client:list')

    if request.method == 'POST':
        message = MessageForm(request.POST)
        Message.objects.create(
            message=message.data.get('message'),
            header=message.data.get('header'),
            user=model)

        return redirect('client:list')
    else:
        request.pk = pk
        message = MessageForm(request.POST)
        return render(request, 'message/sendmessage.html', {
            'form': message
        })


@login_required
def readmessage(request, pk):
    try:
        msg = Message.objects.get(id=pk)
    except Message.DoesNotExist:
        return redirect('message:messages')

    if request.user != msg.user:
        return redirect('errors:permission')
    else:
        msg.readed = True
        msg.save()
        return render(request, 'message/message.html', {
            'msg': msg
        })


@login_required
def updatemsg(request):
    try:
        mymessages = Message.objects.all().filter(user=request.user, readed=False)

        if mymessages:
            return JsonResponse({'data': True, 'count': len(mymessages)})
        else:
            return JsonResponse({'data': False})

    except Exception:
        return JsonResponse({'data':False})


@login_required
def messages(request):
    try:
        mymessages = Message.objects.all().filter(user=request.user).order_by('-id')

        return render(request, 'message/messages.html', {
            'messages': mymessages
        })
    except:
        return render(request, 'message/messages.html')


@login_required
def delete(request, pk):
    try:
        msg = Message.objects.get(id=pk)
        if request.user != msg.user:
            return redirect('errors:permission')
        else:
            msg.delete()
            return redirect('message:messages')
    except Message.DoesNotExist:
        return redirect('message:messages')
