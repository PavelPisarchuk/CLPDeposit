from django import forms
from app.models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'father_name', 'passport_id', 'password']


class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        exclude=['is_archive']


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'


class SavingsDepositForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields='__all__'


class DemandDepositForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ['is_prolongation']