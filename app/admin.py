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


class MessageAdmin(admin.ModelAdmin):
    list_display = (u'id', 'message', 'header', 'readed', 'user', 'date')
    list_filter = ('readed', 'user', 'date')


class DepositAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'depositType',
        'title',
        'description',
        'currency',
        'min_amount',
        'duration',
        'is_pay_period_month',
        'pay_period',
        'percent',
        'is_refill',
        'min_refill',
        'is_early_withdrawal',
        'minimum_balance',
        'percent_for_early_withdrawal',
        'is_capitalization',
        'binding_currency',
        'is_archive',
    )
    list_filter = (
        'currency',
        'is_pay_period_month',
        'is_refill',
        'is_early_withdrawal',
        'is_capitalization',
        'binding_currency',
        'is_archive',
    )


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'deposit',
        'bill',
        'deposit_bill',
        'bonus',
        'sign_date',
        'end_date',
        'is_prolongation',
    )
    list_filter = (
        'deposit',
        'bill',
        'sign_date',
        'end_date',
        'is_prolongation',
    )


class ActionTypeAdmin(admin.ModelAdmin):
    list_display = (u'id', 'description')


class ActionAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'actionType',
        'contract',
        'bill',
        'datetime',
        'money',
    )
    list_filter = ('actionType', 'contract', 'bill', 'datetime')


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (u'id', 'date', 'from_currency', 'to_currency', 'index')
    list_filter = ('date', 'from_currency', 'to_currency')


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.User, UserAdmin)
_register(models.Currency, CurrencyAdmin)
_register(models.Bill, BillAdmin)
_register(models.Card, CardAdmin)
_register(models.Message, MessageAdmin)
_register(models.Deposit, DepositAdmin)
_register(models.Contract, ContractAdmin)
_register(models.ActionType, ActionTypeAdmin)
_register(models.Action, ActionAdmin)
_register(models.ExchangeRate, ExchangeRateAdmin)
