#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from app.models import User,Bill


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'father_name', 'passport_id', 'password']


class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class MessageForm(forms.Form):
    message = forms.CharField(max_length=300, label='Сообщение')
    header = forms.CharField(max_length=100, label='Заголовок')

class SearchForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    passport_id = forms.CharField(max_length=14, label='Идентификационный номер')