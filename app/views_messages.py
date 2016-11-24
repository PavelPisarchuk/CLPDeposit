from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from app.decorators import Only_Superuser_Permission
from app.models import User, Message
from app.forms import MessageForm, SearchForm


@Only_Superuser_Permission
@login_required
def send_message(request, pk):
    try:
        model = User.objects.get(id=pk)
    except User.DoesNotExist:
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False),
            'form': SearchForm(request.POST)
        })

    if request.method == 'POST':
        message = MessageForm(request.POST)
        Message.objects.create(
            message=message.data.get('message'),
            header=message.data.get('header'),
            user=model)

        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False),
            'form': SearchForm(request.POST)
        })
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
        return messages(request)

    if request.user != msg.user:
        return render(request, 'errors/permissionerror.html')
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
        mymessages = Message.objects.all().filter(user=request.user)

        return render(request, 'message/messages.html', {
            'messages': mymessages
        })
    except:
        return render(request, 'message/messages.html')
