# -*- coding: utf-8 -*-
from django import forms

from app.models import Contract, Currency, Deposit, User


class UserForm(forms.ModelForm):
    passport_date = forms.DateField(input_formats=['%d-%m-%Y'])
    birthday = forms.DateField(input_formats=['%d-%m-%Y'])
    class Meta:
        model = User
        fields = ["username", "password", "email",
                  "last_name", "first_name", "father_name",
                  "passport_id", "passport_ser",
                  "address", "phone"]


class EditUserForm(forms.ModelForm):
    passport_date = forms.DateField(input_formats=['%d-%m-%Y'])

    class Meta:
        model = User
        fields = ["email",
                  "last_name", "first_name", "father_name",
                  "passport_date", "passport_id", "passport_ser",
                  "address", "phone"]


class DoVostredDepositForm(forms.ModelForm):
    min_amount=forms.IntegerField(min_value=1,max_value=1000000,label='Минимальная начальная сумма')
    pay_period=forms.IntegerField(min_value=1,max_value=100,label='Период выплат')
    percent = forms.FloatField(min_value=0.1, max_value=500, label='Процентная ставка')
    #percent_for_early_withdrawal=forms.FloatField(min_value=0.1, max_value=500, label='Процентная ставка при нарушении неснижаемого остатка')
    min_refill=forms.IntegerField(min_value=0,max_value=1000000,label='Минимальное пополнение',initial=0)
    class Meta:
        model = Deposit
        exclude = ["duration","is_early_withdrawal","minimum_balance",\
                                                "percent_for_early_withdrawal","binding_currency"]


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
