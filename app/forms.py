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
        fields = ['title', 'description', 'depositType', 'percent', 'percent_for_early_withdrawal', 'is_floating_rate',
                   'min_amount', 'duration', 'min_refill', 'pay_period_in_months', 'is_capitalization', 'minimum_balance',
                  'currency', 'binding_currency']


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['deposit_bill']