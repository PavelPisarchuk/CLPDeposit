# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from app.views import actions, bill, client, contract, deposit, employee, errors, general, messages, profile, rate

urlpatterns = [
    url(r'^login/', general.login, name='login'),
    url(r'^logout/', general.logout, name='logout'),
    url(r'^profile/', include([
        url(r'^info/', profile.info, name='info'),
        url(r'^edit/', profile.edit, name='edit'),
        url(r'^password/', profile.password, name='password'),
    ], namespace='profile')),
    url(r'^rate/', include([
        url(r'^today/', rate.today, name='today'),
    ], namespace='rate')),
    url(r'^message/', include([
        url(r'^send/', messages.send_message, name='send'),
        url(r'^updatemsg/', messages.updatemsg, name='updatemsg'),
        url(r'^messages/', messages.messages, name='messages'),
        url(r'^readmsg/', messages.readmessage, name='readmsg'),
        url(r'^delete/', messages.delete, name='delete'),
    ], namespace='message')),
    url(r'^employee/', include([
        url(r'^new/', employee.new, name='new'),
        url(r'^list/', employee.list, name='list'),
        url(r'^edituser/', employee.edit_user, name='uedit'),
    ], namespace='employee')),
    url(r'^client/', include([
        url(r'^new/', client.new, name='new'),
        url(r'^list/', client.list, name='list'),
        url(r'^search/', client.search, name='search'),
    ], namespace='client')),
    url(r'^actions/', include([
        url(r'^bill/', actions.bill, name='bill'),
        url(r'^contract/', actions.contract, name='contract'),
    ], namespace='actions')),
    url(r'^bill/', include([
        url(r'^bills/', bill.bills, name='bills'),
        url(r'^addbill/', bill.addbill, name='addbill'),
        url(r'^addonbill/', bill.addonbill, name='addonbill'),
        url(r'^billtransact/', bill.billtransact, name='billtransact'),
        url(r'^getuserbills/', bill.getuserbills, name='getuserbills'),
        url(r'^getcurrency/', bill.getcurrency, name='getcurrency'),
        url(r'^getuserbillsfromuser/', bill.getuserbillsfromuser, name='getuserbills'),
    ], namespace='bill')),
    url(r'^deposit/', include([
        url(r'^list/(?P<deposit_id>[0-9]+)/', deposit.list, name='listToArch'),
        url(r'^list/', deposit.list, name='list'),
        url(r'^new/(?P<deposit_id>[0-9]+)/', deposit.new, name='new'),
        url(r'^edit/(?P<deposit_id>[0-9]+)/', deposit.edit, name='edit'),
        url(r'^info/(?P<deposit_id>[0-9]+)/', deposit.info, name='info'),
        url(r'^all/', deposit.all, name='all'),
    ], namespace='deposit')),
    url(r'^contract/', include([
        url(r'^all/', contract.all, name='all'),
        url(r'^new/(?P<deposit_id>[0-9]+)', contract.new, name='new'),
        url(r'^list/', contract.list, name='list'),
        url(r'^addmoney/', contract.addmoney, name='addmoney'),
        url(r'^info/(?P<deposit_id>[0-9]+)', contract.info, name='info'),
    ], namespace='contract')),
    url(r'errors/', include([
        url('r^error/', errors.error, name='error')
    ], namespace='errors')),
    url(r'', general.index, name='index'),
]
