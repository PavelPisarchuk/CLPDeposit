# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.models import Bill, Action


@login_required
def bill(request, pk=None):
    try:
        bill = Bill.objects.get(id=pk, client=request.user)
        return render(request, 'actions/list.html', {
            'info': bill.toString(),
            'operations': Action.objects.all().filter(bill=bill).order_by('-id')
        })
    except Bill.DoesNotExist:
        return redirect('bill:bills')
