# -*- coding: utf-8 -*-
from django.conf.urls import url, include

import app.views.actions as actions
import app.views.bill as bill
import app.views.client as client
import app.views.contract as contract
import app.views.deposit as deposit
import app.views.employee as admin
import app.views.errors as errors
import app.views.general as general
import app.views.messages as messages

urlpatterns = [
    url(r'^login/', general.login, name='login'),
    url(r'^logout/', general.logout, name='logout'),
    url(r'^rates/', general.rates, name='rates'),
    url(r'^password/', general.password, name='password'),
    url(r'^message/', include([
        url(r'^send/', messages.send_message, name='send'),
        url(r'^updatemsg/', messages.updatemsg, name='updatemsg'),
        url(r'^messages/', messages.messages, name='messages'),
        url(r'^readmsg/', messages.readmessage, name='readmsg'),
        url(r'^delete/', messages.delete, name='delete'),
    ], namespace='message')),
    url(r'^employee/', include([
        url(r'^new/', admin.new, name='new'),
        url(r'^list/', admin.list, name='list'),
        url(r'^info/', admin.info, name='info'),
        url(r'^edit/', admin.edit, name='edit'),
        url(r'^edituser/', admin.edit_user, name='uedit'),
    ], namespace='employee')),
    url(r'^client/', include([
        url(r'^list/', client.list, name='list'),
        url(r'^new/', client.new, name='new'),
        url(r'^info/', client.info, name='info'),
        url(r'^edit/', client.edit, name='edit'),
        url(r'^search/', client.search, name='search'),
        url(r'^search/(?P<first_name>\w+)/(?P<last_name>\w+)/(?P<passport_id>\w+/$)', client.search, name='search'),
    ], namespace='client')),
    url(r'^actions/', include([
        url(r'^bill/', actions.bill, name='bill'),
        url(r'^contract/', actions.contract, name='contract'),
    ], namespace='actions')),
    url(r'^bill/', include([
        url(r'^bills/', bill.bills, name='bills'),
        url(r'^addbill/', bill.addbill, name='addbill'),
        url(r'^cards/', bill.cards, name='cards'),
        url(r'^addcard/', bill.addcard, name='addcard'),
        url(r'^addonbill/', bill.addonbill, name='addonbill'),
        url(r'^cardsinbill/(?P<pk>[0-9]+)/$', bill.cardsinbill, name='cardsinbill'),
        url(r'^billoperations/(?P<pk>[0-9]+)/$', bill.billoperations, name='billoperations'),
        url(r'^billtransact/', bill.billtransact, name='billtransact'),
        url(r'^getuserbills/(?P<pk>[0-9]+)/$', bill.getuserbills, name='getuserbills'),
    ], namespace='bill')),
    url(r'^deposit/', include([
        url(r'^list/(?P<deposit_id>[0-9]+)/', deposit.list, name='listToArch'),
        url(r'^list/', deposit.list, name='list'),
        url(r'^new/', deposit.new, name='new'),
        url(r'^edit/(?P<deposit_id>[0-9]+)/', deposit.edit, name='edit'),


        url(r'^refill/', deposit.refill, name='refill'),
        url(r'^transfer/', deposit.transfer, name='transfer'),
        url(r'^close/', deposit.close, name='close'),
        url(r'^extract/', deposit.extract, name='extract'),
        url(r'^history/', deposit.history, name='history')
    ], namespace='deposit')),
    url(r'^contract/', include([
        url(r'^all/', contract.all, name='all'),
        url(r'^new/(?P<deposit_id>[0-9]+)', contract.new, name='new'),
        url(r'^list/', contract.list, name='list'),
        url(r'^info/(?P<deposit_id>[0-9]+)', contract.info, name='info'),
    ], namespace='contract')),
    url(r'errors/', include([
        url('r^error/', errors.error, name='error')
    ], namespace='errors')),
    url(r'', general.index, name='index'),
]
