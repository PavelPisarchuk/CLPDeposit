# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

from app.models import Bill


@login_required
def bill(request):
    # try:
    bill = Bill.objects.get(id=request.POST['num'], client=request.user)
    opers, date, money = [], [], []
    for i in bill.get_actions().order_by('-id'):
        opers.append(i.actionType.description)
        date.append(i.datetime.strftime("%A, %d. %B %Y %I:%M%p"))
        money.append(i.format_money())
    return JsonResponse({'info': bill.toString(), 'operations': opers, 'dates': date, 'money': money})
    # except :
        return redirect('bill:bills')
