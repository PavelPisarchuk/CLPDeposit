from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.models import User, Message


@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_message(request, pk=None):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return redirect('client:list')

    if request.method == 'POST':
        message = request.POST['message']
        header = request.POST['header']
        Message.objects.create(
            message=message,
            header=header,
            user=user)
        return redirect('client:list')


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
