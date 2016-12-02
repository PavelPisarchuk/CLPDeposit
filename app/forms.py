# -*- coding: utf-8 -*-
from django import forms

from app.models import Contract, Currency, Deposit, User

userfields = ["username", "password"]
adminfields = ["email"]
clientfields = ["last_name", "first_name", "father_name",
                "passport_date", "passport_id", "passport_ser",
                "address", "birthday", "phone"]


class UserForm(forms.ModelForm):
    passport_date = forms.DateField(input_formats=['%d/%m/%Y'])
    birthday = forms.DateField(input_formats=['%d/%m/%Y'])
    class Meta:
        model = User
        fields = ["username", "password",
                  "last_name", "first_name", "father_name",
                  "passport_id", "passport_ser",
                  "address", "phone"]


class MessageForm(forms.Form):
    message = forms.CharField(max_length=300, label='Сообщение')
    header = forms.CharField(max_length=100, label='Заголовок')


class SearchForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    passport_id = forms.CharField(max_length=14, label='Идентификационный номер')


class DepositForm(forms.ModelForm):

    class Meta:
        model = Deposit
        exclude = ['is_archive']


class CurrencyForm(forms.ModelForm):

    class Meta:
        model = Currency
        fields = '__all__'


class SavingsDepositForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = '__all__'


class DemandDepositForm(forms.ModelForm):

    class Meta:
        model = Contract
        exclude = ['is_prolongation']
