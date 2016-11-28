# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def error(request):
    return render(request, 'errors/error.html')
