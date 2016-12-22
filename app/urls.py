# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from app.views import actions, bill, client, contract, deposit, employee, general, messages, profile, rate

urlpatterns = [
    url(r'^login/', general.login, name='login'),
    url(r'^logout/', general.logout, name='logout'),
    url(r'^profile/', include([
        url(r'^info/', profile.info, name='info'),
        url(r'^edit/', profile.edit, name='edit'),
        url(r'^password/', profile.password, name='password'),
        url(r'^setpassword/(?P<id>[0-9]+)/', profile.setpassword, name='setpassword'),
    ], namespace='profile')),
    url(r'^rate/', include([
        url(r'^today/', rate.today, name='today'),
        url(r'^api/', rate.api, name='api'),
        url(r'^history/', rate.api_history, name='history'),
    ], namespace='rate')),
    url(r'^message/', include([
        url(r'^send/', messages.send_message, name='send'),
        url(r'^messages/', messages.messages, name='messages'),
        url(r'^readmsg/', messages.readmessage, name='readmsg'),
        url(r'^delete/', messages.delete, name='delete'),
    ], namespace='message')),
    url(r'^employee/', include([
        url(r'^new/', employee.new, name='new'),
        url(r'^list/', employee.list, name='list'),
        url(r'^edituser/', employee.edit_user, name='uedit'),
        url(r'^stats/', employee.stats, name='stats'),
        url(r'^statistics/', employee.statistics, name='statistics'),
    ], namespace='employee')),
    url(r'^client/', include([
        url(r'^new/', client.new, name='new'),
        url(r'^list/', client.list, name='list'),
        url(r'^partiallist/', client.partiallist, name='partiallist'),
        url(r'^partiallistsearch/', client.partiallistsearch, name='partiallistsearch'),
        url(r'^search/', client.search, name='search'),
        url(r'^info/', client.info, name='info'),
        url(r'^getlistlen/', client.getlistlen, name='getlistlen'),
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
        url(r'^userbillinfo/', bill.userbillinfo, name='userbillinfo'),
        url(r'^usercontracts/', bill.usercontracts, name='usercontracts'),
        url(r'^closebill/', bill.closebill, name='closebill'),
    ], namespace='bill')),
    url(r'^deposit/', include([
        url(r'^list/(?P<deposit_id>[0-9]+)/', deposit.list, name='listToArch'),
        url(r'^list/', deposit.list, name='list'),
        url(r'^new/(?P<deposit_id>[0-9]+)/', deposit.new, name='new'),
        url(r'^edit/(?P<deposit_id>[0-9]+)/', deposit.edit, name='edit'),
        url(r'^all/', deposit.all, name='all'),
    ], namespace='deposit')),
    url(r'^contract/', include([
        url(r'^all/', contract.all, name='all'),
        url(r'^new/(?P<deposit_id>[0-9]+)', contract.new, name='new'),
        url(r'^list/', contract.list, name='list'),
        url(r'^addmoney/', contract.addmoney, name='addmoney'),
        url(r'^close/', contract.close, name='close'),
        url(r'^submoney/', contract.submoney, name='submoney'),
    ], namespace='contract')),
    url(r'^jump/(?P<count>[0-9]+)/', general.jump, name='jump'),
    url(r'^load/', general.load, name='load'),
    url(r'', general.index, name='index'),
]
