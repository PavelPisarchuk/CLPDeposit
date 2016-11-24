# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):

    list_display = (
        u'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'father_name',
        'passport_id',
        'phone',
        'address',
        'birthday',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'birthday',
    )
    raw_id_fields = ('groups', 'user_permissions')


class CurrencyAdmin(admin.ModelAdmin):

    list_display = (u'id', 'title', 'icon')


class BillAdmin(admin.ModelAdmin):

    list_display = (u'id', 'client', 'money', 'currency')
    list_filter = ('client', 'currency')


class CardAdmin(admin.ModelAdmin):

    list_display = (u'id', 'bill', 'limit')
    list_filter = ('bill',)


class MessageBoxAdmin(admin.ModelAdmin):

    list_display = (u'id', 'user')
    list_filter = ('user',)


class MessageAdmin(admin.ModelAdmin):

    list_display = (
        u'id',
        'message',
        'header',
        'readed',
        'messagebox',
        'date',
    )
    list_filter = ('readed', 'messagebox', 'date')


class DepositAdmin(admin.ModelAdmin):

    list_display = (
        u'id',
        'title',
        'description',
        'percent',
        'min_storing_term',
        'max_storing_term',
        'pay_term',
        'refill',
        'partial_take',
        'indexed',
        'currency',
    )
    list_filter = ('refill', 'partial_take', 'indexed', 'currency')


class ContractAdmin(admin.ModelAdmin):

    list_display = (u'id', 'bill', 'deposit', 'sign_date', 'term', 'money')
    list_filter = ('bill', 'deposit', 'sign_date')


class PayAdmin(admin.ModelAdmin):

    list_display = (u'id', 'agent', 'contract', 'datetime', 'money')
    list_filter = ('agent', 'contract', 'datetime')


class ExchangeRateAdmin(admin.ModelAdmin):

    list_display = (u'id', 'date', 'from_currency', 'to_currency', 'index')
    list_filter = ('date', 'from_currency', 'to_currency')


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.User, UserAdmin)
_register(models.Currency, CurrencyAdmin)
_register(models.Bill, BillAdmin)
_register(models.Card, CardAdmin)
_register(models.MessageBox, MessageBoxAdmin)
_register(models.Message, MessageAdmin)
_register(models.Deposit, DepositAdmin)
_register(models.Contract, ContractAdmin)
_register(models.Pay, PayAdmin)
_register(models.ExchangeRate, ExchangeRateAdmin)
