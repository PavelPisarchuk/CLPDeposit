# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import Bill, Contract


@login_required
def bill(request):
    try:
        if not request.user.is_superuser:
            bill_actions = Bill.objects.get(
                id=request.POST['num'],
                client=request.user
            ).get_actions().order_by('-id')
        else:
            bill_actions = Bill.objects.get(
                id=request.POST['num']
            ).get_actions().order_by('-id')
    except:
        bill_actions = {}
    finally:
        return render(request, 'bill/bill_operations.html', {
            'bills': bill_actions
        })


@login_required
def contract(request):
    try:
        if not request.user.is_superuser:
            contracts = Contract.objects.get(
                id=request.POST['num'],
                bill__client=request.user
            ).get_actions().order_by('-id')
        else:
            contracts = Contract.objects.get(
                id=request.POST['num']
            ).get_actions().order_by('-id')
    except:
        contracts = {}
    finally:
        return render(request, 'actions/contract_operations.html', {
            'contracts': contracts
        })
