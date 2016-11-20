from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from app.decorators import Only_Superuser_Permission
from django.db.models import Q
from django.http import JsonResponse

from app.views import index
from app.models import User, Bill, Currency, Message, MessageBox
from app.forms import UserForm, clientfields


@login_required
@Only_Superuser_Permission
def new(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
        return redirect(index)
    else:
        return render(request, 'client/registration.html', {
            'form': UserForm()
        })


@login_required
@Only_Superuser_Permission
def list(request):
    return render(request, 'client/list.html', {
        'clients': User.objects.all().filter(is_superuser=False)
    })

@login_required
@Only_Superuser_Permission
def search(request):
    from app.forms import SearchForm

    if(request.POST):
        users = User.objects.all()
        Form = SearchForm(request.POST)
        #print(Form.data.get('first_name'))

        if(Form.data.get('first_name')):
            users=users.filter(first_name__contains=Form.data.get('first_name'))
        if(Form.data.get('last_name')):
            users=users.filter(last_name__contains=Form.data.get('last_name'))
        if(Form.data.get('passport_id')):
            users=users.filter(passport_id__contains=Form.data.get('passport_id'))


        return render(request,'client/list.html', {
            'form':Form,'clients': users.filter(is_superuser=False)
        })
    else:
        return render(request, 'client/list.html', {
            'clients': User.objects.all().filter(is_superuser=False), 'form': SearchForm()
        })


@login_required
def info(request):
    Form = modelform_factory(User, fields=clientfields)
    return render(request, 'client/info.html', {
        'form': Form(instance=request.user)
    })


@login_required
def edit(request):
    Form = modelform_factory(User, fields=clientfields)
    user = request.user

    if request.method == 'POST':
        form = Form(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect(index)
    else:
        return render(request, 'client/edit.html', {
            'form': Form(instance=user)
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
        return render(request, 'client/message.html', {'msg':msg })


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
            return JsonResponse({'data': True,'count':count})
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
        return render(request, 'client/messages.html', {'messages'
                                                        : reversed(mymessages)})
    except:
        return render(request, 'client/messages.html')
