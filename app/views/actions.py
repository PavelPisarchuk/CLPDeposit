# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.models import Bill


@login_required
def bill(request, pk=None):
    try:
        bill = Bill.objects.get(id=pk, client=request.user)
        return render(request, 'actions/list.html', {
            'info': bill.toString(),
            'operations': bill.get_actions().order_by('-id')
        })
    except Bill.DoesNotExist:
        return redirect('bill:bills')
