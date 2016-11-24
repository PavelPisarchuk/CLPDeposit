from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from app.decorators import Only_Superuser_Permission
from app.models import User, Message, MessageBox
from app.forms import MessageForm, SearchForm


@Only_Superuser_Permission
@login_required
def send_message(request, pk):
    try:
        model = User.objects.get(id=pk)
    except User.DoesNotExist:
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False),'form': SearchForm(request.POST)
        })

    if request.method == 'POST':
        try:
            messageBox = MessageBox.objects.get(user_id=pk)
        except MessageBox.DoesNotExist:
            messageBox = MessageBox.objects.create(user=model)

        message=MessageForm(request.POST)
        Message.objects.create(message=message.data.get('message'),header=message.data.get('header'),
                               readed=False,messagebox=messageBox)

        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False),'form': SearchForm(request.POST)
        })
    else:
        request.pk = pk
        message = MessageForm(request.POST)
        return render(request, 'message/sendmessage.html', {
            'form': message
        })


@login_required
def readmessage(request,pk):
    try:
        msg=Message.objects.get(id=pk)
    except Message.DoesNotExist:
        return messages(request)

    if request.user.id!=msg.messagebox.user_id:
        return render(request,'errors/permissionerror.html')
    else:
        msg.readed=True
        msg.save()
        return render(request, 'message/message.html', {
            'msg': msg
        })


@login_required
def updatemsg(request):
    try:
        messageBox=MessageBox.objects.get(user_id=request.user.id)
        mymessages=Message.objects.all().filter(messagebox_id__exact=messageBox.id)
        count=0
        for msg in mymessages:
            if msg.readed==False:
                count+=1

        if count>0:
            return JsonResponse({'data': True, 'count': count})
        else:
            return JsonResponse({'data': False})

    except messageBox.DoesNotExist:
        return JsonResponse({'data':False})


@login_required
def messages(request):
    try:
        messageBox=MessageBox.objects.get(user_id=request.user.id)
        mymessages=Message.objects.all().filter(messagebox_id__exact=messageBox.id).reverse()
        for msg in mymessages:
            if msg.readed==False:
                request.msgtext='q'
                break
        return render(request, 'message/messages.html', {
            'messages': reversed(mymessages)
        })
    except:
        return render(request, 'message/messages.html')
